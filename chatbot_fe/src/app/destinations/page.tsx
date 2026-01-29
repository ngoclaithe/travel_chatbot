'use client';

import React, { useEffect, useState } from 'react';
import { DestinationCard } from '@/components/cards/DestinationCard';
import { Destination } from '@/types';
import axiosClient from '@/lib/axiosClient';
import { Skeleton } from '@/components/ui/skeleton';
import { AlertCircle } from 'lucide-react';

export default function DestinationsPage() {
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDestinations();
  }, []);

  const fetchDestinations = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await axiosClient.get<Destination[]>('/destinations/');
      // console.log('Response:', response.data);

      if (Array.isArray(response.data)) {
        setDestinations(response.data);
      } else {
        console.warn('Unexpected response format:', response.data);
        setDestinations([]);
      }

    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Không thể tải điểm đến'
      );
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <div className="min-h-screen bg-white dark:bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-ocean-blue to-ocean-light text-white py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Khám Phá Điểm Đến 🗺️
          </h1>
          <p className="text-lg opacity-90">
            Khám phá những nơi đẹp nhất để thăm viếng trên khắp thế giới
          </p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        {error && (
          <div className="bg-destructive/10 border border-destructive text-destructive p-4 rounded-lg mb-8 flex items-center gap-3">
            <AlertCircle className="w-5 h-5" />
            <span>{error}</span>
          </div>
        )}

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: 6 }).map((_, i) => (
              <Skeleton key={i} className="h-80 rounded-lg" />
            ))}
          </div>
        ) : destinations.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground text-lg">
              Không tìm thấy điểm đến nào. Vui lòng thử lại sau.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {destinations.map((destination) => (
              <DestinationCard
                key={destination.id}
                destination={destination}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
