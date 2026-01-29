'use client';

import React, { useEffect, useState } from 'react';
import { TourCard } from '@/components/cards/TourCard';
import { Tour } from '@/types';
import axiosClient from '@/lib/axiosClient';
import { Skeleton } from '@/components/ui/skeleton';
import { AlertCircle } from 'lucide-react';

export default function ToursPage() {
  const [tours, setTours] = useState<Tour[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTours();
  }, []);

  const fetchTours = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await axiosClient.get('/tours');
      if (Array.isArray(response.data.data)) {
        setTours(response.data.data);
      } else if (Array.isArray(response.data)) {
        setTours(response.data);
      } else {
        setTours([]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Không thể tải tour du lịch');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-background">
      <div className="bg-gradient-to-r from-ocean-blue to-ocean-light text-white py-12 px-4">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Khám Phá Tour Du Lịch ✈️
          </h1>
          <p className="text-lg opacity-90">
            Duyệt qua bộ sưu tập tour du lịch tuyệt vời được lựa chọn cẩn thận
          </p>
        </div>
      </div>

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
        ) : tours.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground text-lg">
              Không tìm thấy tour nào. Vui lòng thử lại sau.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tours.map((tour) => (
              <TourCard
                key={tour.id}
                tour={{
                  ...tour,
                  destinations:
                    typeof tour.destinations === 'string'
                      ? [tour.destinations]
                      : Array.isArray(tour.destinations)
                        ? tour.destinations
                        : [],
                }}
              />
            ))}

          </div>
        )}
      </div>
    </div>
  );
}
