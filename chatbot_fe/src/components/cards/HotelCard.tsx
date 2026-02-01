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
            unoptimized
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

          {(() => {
            let amenitiesList: string[] = [];

            const parseItem = (item: any): string[] => {
              if (!item) return [];
              if (typeof item !== 'string') return [String(item)];

              const trimmed = item.trim();

              // Try JSON Array
              if (trimmed.startsWith('[')) {
                try {
                  const parsed = JSON.parse(trimmed);
                  if (Array.isArray(parsed)) return parsed.flatMap(parseItem);
                } catch { }
              }

              // Try Postgres Array {a,b,c}
              if (trimmed.startsWith('{') && trimmed.endsWith('}')) {
                const content = trimmed.slice(1, -1);
                if (!content) return [];
                return content.split(',').map(s => s.trim().replace(/^"|"$|'/g, ''));
              }

              // Try comma separated if it looks like a list
              if (trimmed.includes(',')) {
                return trimmed.split(',').map(s => s.trim());
              }

              return [trimmed];
            };

            if (hotel.amenities) {
              if (Array.isArray(hotel.amenities)) {
                amenitiesList = hotel.amenities.flatMap(parseItem);
              } else {
                amenitiesList = parseItem(hotel.amenities);
              }
            }

            // Deduplicate
            amenitiesList = Array.from(new Set(amenitiesList)).filter(Boolean);

            if (amenitiesList.length > 0) {
              return (
                <div className="pt-2 border-t border-border">
                  <p className="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2">
                    Amenities:
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {amenitiesList.slice(0, 3).map((amenity, idx) => (
                      <span
                        key={`${amenity}-${idx}`}
                        className="text-xs bg-ocean-light/10 text-ocean-blue px-2 py-1 rounded"
                      >
                        {amenity}
                      </span>
                    ))}
                    {amenitiesList.length > 3 && (
                      <span className="text-xs text-muted-foreground px-2 py-1">
                        +{amenitiesList.length - 3} more
                      </span>
                    )}
                  </div>
                </div>
              );
            }
            return null;
          })()}
        </div>
      </CardContent>
    </Card>
  );
};
