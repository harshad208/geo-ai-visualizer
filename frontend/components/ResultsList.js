'use client';

import { Skeleton } from '@/components/ui/skeleton.jsx';

const ResultsList = ({ geoJsonData, isLoading, onItemClick, selectedItem }) => {

  if (isLoading) {
    return Array(5).fill(0).map((_, index) => (
      <div key={index} className="flex items-center space-x-4 p-3">
        <Skeleton className="h-10 w-10 rounded-lg" />
        <div className="space-y-2">
          <Skeleton className="h-4 w-[200px]" />
          <Skeleton className="h-4 w-[150px]" />
        </div>
      </div>
    ));
  }
  
  return (
  <div className="p-2 pt-0">
    {geoJsonData.map((feature, index) => {
      const properties = feature.properties;
      const isSelected = selectedItem?.properties.place_name === properties.place_name; 

      return (
        <div
          key={index}
          onClick={() => onItemClick(feature)}
          className={`p-3 rounded-lg cursor-pointer transition-colors hover:bg-accent ${isSelected ? 'bg-accent' : ''}`}
        >
          <p className="font-semibold">{properties.place_name}</p> {/* Use place_name */}
          <p className="text-sm text-muted-foreground">
            {properties.city} | Type: <span className="font-medium">{properties.entity_type}</span>
          </p>
        </div>
      );
    })}
  </div>
);
};

export default ResultsList;