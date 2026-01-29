'use client';

import React, { useEffect, useState } from 'react';
import { HotelCard } from '@/components/cards/HotelCard';
import { Hotel } from '@/types';
import axiosClient from '@/lib/axiosClient';
import { Skeleton } from '@/components/ui/skeleton';
import { AlertCircle } from 'lucide-react';

export default function HotelsPage() {
  const [hotels, setHotels] = useState<Hotel[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHotels();
  }, []);

  const fetchHotels = async () => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await axiosClient.get<Hotel[]>('/hotels');
      console.log('Response:', response.data);

      if (Array.isArray(response.data)) {
        setHotels(response.data);
      } else {
        console.warn('Unexpected response format:', response.data);
        setHotels([]);
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Không thể tải khách sạn');
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
            Đặt Khách Sạn 🏨
          </h1>
          <p className="text-lg opacity-90">
            Tìm nơi ở lý tưởng cho chuyến đi của bạn
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
        ) : hotels.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground text-lg">
              Không tìm thấy khách sạn nào. Vui lòng thử lại sau.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {hotels.map((hotel) => (
              <HotelCard key={hotel.id} hotel={hotel} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
