'use client';

import React, { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/button';
import {
  BarChart3,
  Map,
  Hotel,
  Compass,
  Utensils,
  Activity,
  Cloud,
  Navigation,
  Star,
  LogOut,
  Menu,
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface AdminLayoutProps {
  children: React.ReactNode;
}

const menuItems = [
  { href: '/admin/dashboard', icon: BarChart3, label: 'Bảng Điều Khiển' },
  { href: '/admin/destinations', icon: Map, label: 'Điểm Đến' },
  { href: '/admin/hotels', icon: Hotel, label: 'Khách Sạn' },
  { href: '/admin/tours', icon: Compass, label: 'Tour Du Lịch' },
  { href: '/admin/restaurants', icon: Utensils, label: 'Nhà Hàng' },
  { href: '/admin/activities', icon: Activity, label: 'Hoạt Động' },
  { href: '/admin/weather', icon: Cloud, label: 'Thời Tiết' },
  { href: '/admin/transportation', icon: Navigation, label: 'Vận Tải' },
  { href: '/admin/reviews', icon: Star, label: 'Bình Luận' },
];

export const AdminLayout: React.FC<AdminLayoutProps> = ({ children }) => {
  const router = useRouter();
  const pathname = usePathname();
  const { isAuthenticated, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  useEffect(() => {
    if (!isAuthenticated && pathname !== '/admin/login') {
      router.push('/admin/login');
    }
  }, [isAuthenticated, pathname, router]);

  if (!isAuthenticated && pathname !== '/admin/login') {
    return null;
  }

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <div className="flex h-screen bg-white dark:bg-background">
      {/* Sidebar */}
      <aside
        className={cn(
          'w-64 bg-dark-gray text-white flex flex-col transition-all duration-300',
          isMobileMenuOpen ? 'translate-x-0' : 'md:translate-x-0 -translate-x-full'
        )}
      >
        {/* Logo */}
        <div className="p-6 border-b border-gray-700">
          <Link href="/admin/dashboard" className="flex items-center gap-2">
            <div className="text-2xl">🧳</div>
            <span className="text-lg font-bold">Du Lịch AI - Quản Trị</span>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto py-6 px-3">
          <ul className="space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <li key={item.href}>
                  <Link href={item.href}>
                    <button
                      className={cn(
                        'w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors',
                        isActive
                          ? 'bg-ocean-blue text-white'
                          : 'text-gray-300 hover:bg-gray-700'
                      )}
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      <Icon className="w-5 h-5" />
                      <span>{item.label}</span>
                    </button>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Logout */}
        <div className="p-3 border-t border-gray-700">
          <Button
            onClick={handleLogout}
            variant="outline"
            className="w-full text-white border-gray-600 hover:bg-gray-700"
          >
            <LogOut className="w-4 h-4 mr-2" />
            Đăng Xuất
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Mobile Menu Button */}
        <div className="md:hidden bg-white dark:bg-card border-b border-border p-4">
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
          >
            <Menu className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/50 md:hidden z-20"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </div>
  );
};
