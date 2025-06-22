'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button.jsx'; 
import { Input } from '@/components/ui/input.jsx'; 
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'; 
import { Search, LoaderCircle } from 'lucide-react';

const QueryInterface = ({ onQuerySubmit, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onQuerySubmit(query);
    }
  };

  const exampleQueries = [
    "Most funded startups",
    "Latest unicorn startups",
    "Top AI companies in India",
  ];

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Ask the Map</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="flex items-center gap-2">
          <Input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., Show me the highest funded startups in Bangalore"
            disabled={isLoading}
          />
          <Button type="submit" disabled={isLoading} className="w-28">
            {isLoading ? (
              <LoaderCircle className="animate-spin" />
            ) : (
              <><Search className="mr-2 h-4 w-4" /> Ask</>
            )}
          </Button>
        </form>
        <div className="mt-4 text-sm text-muted-foreground">
          <strong>Try:</strong>
          {exampleQueries.map((q) => (
            <button
              key={q}
              onClick={() => setQuery(q)}
              className="ml-2 underline hover:text-primary transition-colors"
            >
              {q}
            </button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default QueryInterface;