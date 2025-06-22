from fastapi import APIRouter, HTTPException

from app.models.schemas import QueryRequest, QueryResponse
from app.services import nlp_service, data_service, intent_service, scraping_service

router = APIRouter()

ACTION_MAP = {
    "get_all_startups": data_service.get_all_startups,
    "get_top_funded": data_service.get_top_funded,
    "get_startups_by_city": data_service.get_startups_by_city,
}


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Implements an "Intelligent Fallback" approach.
    1. Checks for a local DB match.
    2. If the match is not high-confidence, it tries a web search.
    3. If the web search fails, it falls back to the original DB match if one existed.
    """
    geo_data = []
    action_triggered = "no_action"
    
    db_match_result = nlp_service.find_best_match(request.query)
    low_confidence_db_data = None
    
    if db_match_result and db_match_result[1] >= nlp_service.SIMILARITY_THRESHOLD:
        
        matched_action, score = db_match_result
        action_name = matched_action.get("action")
        params = matched_action.get("params", {})
        data_function = ACTION_MAP[action_name]
        geo_data = data_function(**params)
        action_triggered = f"database_high_confidence_match(score={score:.2f})"
    else:
        
        if db_match_result:
            
            matched_action, _ = db_match_result
            data_function = ACTION_MAP[matched_action.get("action")]
            low_confidence_db_data = data_function(**matched_action.get("params", {}))

        print("Confidence below threshold. Proceeding to LLM-powered web search.")
        search_context = intent_service.extract_search_context(request.query)
        
        if search_context and search_context.search_topic:
            web_search_data = scraping_service.search_and_scrape(
                search_context.search_topic,
                search_context.geographic_context
            )
            
            if web_search_data:
               
                geo_data = web_search_data
                action_triggered = f"web_search_success(topic='{search_context.search_topic}')"
            elif low_confidence_db_data:
                
                print("Web search failed. Falling back to low-confidence database result.")
                geo_data = low_confidence_db_data
                action_triggered = "database_low_confidence_fallback"
    
    if not geo_data:
         action_triggered = "no_results_found"

    return QueryResponse(
        action_triggered=action_triggered,
        data=geo_data
    )