'use client';

import React from 'react';
import Image from 'next/image';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Destination } from '@/types';
import { Star, MapPin } from 'lucide-react';

interface DestinationCardProps {
  destination: Destination;
}

export const DestinationCard: React.FC<DestinationCardProps> = ({ destination }) => {
  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow h-full">
      {destination.image_url && (
        <div className="w-full h-48 bg-gray-200 dark:bg-gray-700 overflow-hidden relative">
          <Image
            src={destination.image_url}
            alt={destination.name}
            fill
            className="object-cover hover:scale-105 transition-transform"
          />
        </div>
      )}
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1">
            <CardTitle className="text-lg">{destination.name}</CardTitle>
            <CardDescription className="flex items-center gap-1 mt-1">
              <MapPin className="w-4 h-4" />
              {destination.province}, {destination.region}
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          {destination.description}
        </p>
        <div className="flex items-center justify-between pt-3 border-t border-border">
          <div className="flex items-center gap-1">
            <Star className="w-4 h-4 text-sand-yellow fill-sand-yellow" />
            <span className="text-sm font-semibold">{destination.rating}</span>
          </div>
          <span className="text-xs text-muted-foreground">
            Best: {destination.best_time_to_visit}
          </span>
        </div>
      </CardContent>
    </Card>
  );
};
