'use client'; 

import { useState, useMemo } from 'react';
import dynamic from 'next/dynamic';
import QueryInterface from '@/components/QueryInterface.js';
import ResultsList from '@/components/ResultsList.js';
import { toast } from "sonner";
import { Skeleton } from '@/components/ui/skeleton.jsx';
import { Button } from '@/components/ui/button.jsx';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible.jsx';
import { Globe, Database, Bot, ChevronsUpDown, SearchX } from 'lucide-react';

export default function Home() {
  const [geoJsonData, setGeoJsonData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [isListOpen, setIsListOpen] = useState(false);
  
  const [queryCompleted, setQueryCompleted] = useState(false);

  const Map = useMemo(() => dynamic(() => import('@/components/Map.js'), { 
    ssr: false,
    loading: () => <Skeleton className="w-full h-full" />
  }), []);

  const handleQuerySubmit = async (query) => {
    setIsLoading(true);
    setQueryCompleted(false); 
    setGeoJsonData([]);
    setSelectedItem(null);
    setIsListOpen(false);

    try {
      const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/v1/query`;
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      if (!response.ok) throw new Error(`API error! status: ${response.status}`);
      
      const result = await response.json();
      setGeoJsonData(result.data);
      
      const isScraped = result.action_triggered.includes('scrape');
      
      toast.success("Query Complete!", {
        description: `Found ${result.data.length} locations. Source: ${isScraped ? 'Live Web Search' : 'Local Database'}.`,
        icon: isScraped ? <Bot className="h-4 w-4" /> : <Database className="h-4 w-4" />,
      });
      
      if (result.data.length > 0) {
        setIsListOpen(true);
      }

    } catch (e) {
      toast.error("Uh oh! Something went wrong.", {
        description: "Could not get an answer from the map. Please try again.",
      });
    } finally {
      setIsLoading(false);
      setQueryCompleted(true); 
    }
  };

  const handleItemClick = (item) => {
    setSelectedItem(item);
    setIsListOpen(false);
  };
  
  
  const renderFloatingPanel = () => {
    if (isLoading || !queryCompleted) {
      return null;
    }

    if (geoJsonData.length > 0) {
      return (
        <Collapsible
          open={isListOpen}
          onOpenChange={setIsListOpen}
          
          className="absolute top-3 left-3 w-[400px] max-w-[90%] bg-background/90 backdrop-blur-sm rounded-lg border shadow-lg z-10"
        >
          <CollapsibleTrigger asChild>
            <div className="p-2">
              <Button variant="outline" className="w-full flex justify-between items-center px-4">
                <span>{`Found ${geoJsonData.length} Results`}</span>
                <ChevronsUpDown className="h-4 w-4" />
              </Button>
            </div>
          </CollapsibleTrigger>
          <CollapsibleContent>
            <div className="max-h-[50vh] overflow-y-auto">
              <ResultsList
                geoJsonData={geoJsonData}
                isLoading={false}
                onItemClick={handleItemClick}
                selectedItem={selectedItem}
              />
            </div>
          </CollapsibleContent>
        </Collapsible>
      );
    }

    return (
      
      <div className="absolute top-3 left-3 z-10">
         <Button variant="outline" disabled className="flex items-center gap-2">
            <SearchX className="h-4 w-4" />
            No results found for your query.
        </Button>
      </div>
    );
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-muted/40">
      <header className="flex items-center gap-4 border-b bg-background p-4 flex-shrink-0">
        <Globe className="h-6 w-6 text-primary" />
        <h1 className="text-xl font-semibold tracking-tight">Geo-AI Visualizer</h1>
      </header>
      
      <main className="flex-1 flex flex-col gap-4 p-4">
        <div className="query-container flex-shrink-0">
          <QueryInterface onQuerySubmit={handleQuerySubmit} isLoading={isLoading} />
        </div>
        
        <div className="flex-1 border rounded-lg overflow-hidden relative">
          <Map geoJsonData={geoJsonData} selectedItem={selectedItem} />
          {renderFloatingPanel()}
        </div>
      </main>
    </div>
  );
}