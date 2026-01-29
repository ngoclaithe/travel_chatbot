// Destinations
export interface Destination {
  id: string;
  name: string;
  province: string;
  region: string;
  rating: number;
  best_time_to_visit: string;
  description: string;
  image_url?: string;
  created_at?: string;
  updated_at?: string;
}

// Hotels
export interface Hotel {
  id: string;
  name: string;
  destination_id: string;
  star_rating: number;
  price_range: string;
  rating: number;
  amenities: string[];
  image_url?: string;
  created_at?: string;
  updated_at?: string;
}

// Tours
export interface Tour {
  id: string;
  name: string;
  destinations: string[];
  duration_days: number;
  price: number;
  description: string;
  image_url?: string;
  created_at?: string;
  updated_at?: string;
}

// Restaurants
export interface Restaurant {
  id: string;
  name: string;
  destination_id: string;
  cuisine_type: string;
  price_range: string;
  rating: number;
  image_url?: string;
  created_at?: string;
  updated_at?: string;
}

// Activities
export interface Activity {
  id: string;
  destination_id?: string;
  type: string;
  price: number;
  duration: string;
  description: string;
  image_url?: string;
  created_at?: string;
  updated_at?: string;
}

// Weather
export interface Weather {
  id: string;
  destination_id: string;
  month: number;
  avg_temp: number;
  description: string;
  is_best_time: boolean;
  created_at?: string;
  updated_at?: string;
}

// Transportation
export interface Transportation {
  id: string;
  from_destination: string;
  to_destination: string;
  type: string;
  duration: string;
  price_range: string;
  created_at?: string;
  updated_at?: string;
}

// Reviews
export interface Review {
  id: string;
  entity_type: 'destination' | 'hotel' | 'restaurant' | 'tour';
  entity_id: string;
  rating: number;
  comment: string;
  author?: string;
  created_at?: string;
  updated_at?: string;
}

// Chat Message
export interface ChatMessage {
  id: string;
  sender: 'user' | 'bot';
  content: string;
  timestamp: string;
  metadata?: {
    intent?: string;
    data?: unknown;
  };
}

// Auth
export interface AuthUser {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
  created_at?: string;
}

// API Response
export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
  code?: string;
}
