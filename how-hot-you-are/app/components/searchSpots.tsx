"use client";
import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';

const TouristSpotsSearch = () => {
  const [searchQuery, setSearchQuery] = useState('');
  
  interface TouristSpot {
    name: string;
    description: string;
    location: string;
  }

  const [spots, setSpots] = useState<TouristSpot[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  interface FetchTouristSpotsResponse {
    tourist_spots: [TouristSpot];
    error?: string;
  }

  const handleSearch = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`http://localhost:5000/get_tourist_spots?city=${encodeURIComponent(searchQuery)}`);
      const data: FetchTouristSpotsResponse = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch tourist spots');
      }
      console.log(data.tourist_spots);
      setSpots(data.tourist_spots);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message || 'An error occurred while fetching tourist spots');
      } else {
        setError('An error occurred while fetching tourist spots');
      }
      setSpots([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Discover Bangladesh
          </h1>
          <p className="text-gray-600">
            Search for tourist spots in different cities of Bangladesh
          </p>
        </div>

        <form onSubmit={handleSearch} className="mb-8">
          <div className="flex gap-2">
            <Input
              type="text"
              placeholder="Enter a city name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1"
            />
            <Button type="submit" disabled={loading}>
              {loading ? (
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Searching...
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <Search className="w-4 h-4" />
                  Search
                </div>
              )}
            </Button>
          </div>
        </form>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {spots.map((spot, index) => (
            <Card key={index}>
              <CardHeader>
                <CardTitle>{spot.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-2">{spot.description}</p>
                <p className="text-sm text-gray-500">
                  Location: {spot.location}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        {spots.length === 0 && !loading && !error && (
          <div className="text-center text-gray-500 mt-8">
            No tourist spots found. Try searching for a different city!
          </div>
        )}
      </div>
    </div>
  );
};

export default TouristSpotsSearch;