'use client';

import React from 'react';
import Image from 'next/image';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Hotel } from '@/types';
import { Star } from 'lucide-react';

interface HotelCardProps {
  hotel: Hotel;
}

export const HotelCard: React.FC<HotelCardProps> = ({ hotel }) => {
  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow h-full">
      {hotel.image_url && (
        <div className="w-full h-48 bg-gray-200 dark:bg-gray-700 overflow-hidden relative">
          <Image
            src={hotel.image_url}
            alt={hotel.name}
            fill
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            className="object-cover hover:scale-105 transition-transform"
          />
        </div>
      )}
      <CardHeader className="pb-3">
        <CardTitle className="text-lg">{hotel.name}</CardTitle>
        <CardDescription className="flex items-center gap-1">
          {Array.from({ length: hotel.star_rating }).map((_, i) => (
            <Star
              key={i}
              className="w-4 h-4 text-sand-yellow fill-sand-yellow"
            />
          ))}
          <span className="ml-2 text-xs">({hotel.rating} rating)</span>
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Giá tham khảo:
            </span>
            <span className="flex items-center gap-1 font-semibold text-ocean-blue">
              {hotel.price_range} VNĐ
            </span>
          </div>

          {hotel.amenities && hotel.amenities.length > 0 && (
            <div className="pt-2 border-t border-border">
              <p className="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Amenities:
              </p>
              <div className="flex flex-wrap gap-1">
                {hotel.amenities.slice(0, 3).map((amenity) => (
                  <span
                    key={amenity}
                    className="text-xs bg-ocean-light/10 text-ocean-blue px-2 py-1 rounded"
                  >
                    {amenity}
                  </span>
                ))}
                {hotel.amenities.length > 3 && (
                  <span className="text-xs text-muted-foreground px-2 py-1">
                    +{hotel.amenities.length - 3} more
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
