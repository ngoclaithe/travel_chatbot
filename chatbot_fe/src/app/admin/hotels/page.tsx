'use client';

import React, { useEffect, useState } from 'react';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { DataTable, ColumnDef } from '@/components/admin/DataTable';
import { EntityForm } from '@/components/admin/EntityForm';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useAdminCRUD } from '@/hooks/useAdminCRUD';
import { Hotel } from '@/types';
import { z } from 'zod';

const hotelSchema = z.object({
  name: z.string().min(2, 'Tên phải có ít nhất 2 ký tự'),
  destination_id: z.string().min(1, 'Điểm đến là bắt buộc'),
  star_rating: z.coerce.number().min(1).max(5, 'Xếp hạng sao phải từ 1 đến 5'),
  price_range: z.string().min(1, 'Phạm vi giá là bắt buộc'),
  rating: z.coerce.number().min(0).max(5, 'Đánh giá phải từ 0 đến 5'),
  amenities: z.string().optional(),
  image_url: z.string().url('Phải là một URL hợp lệ').optional().or(z.literal('')),
});

type HotelFormData = z.infer<typeof hotelSchema>;

const columns: ColumnDef<Hotel>[] = [
  { key: 'name', label: 'Tên Khách Sạn' },
  {
    key: 'image_url',
    label: 'Hình Ảnh',
    render: (value) => value ? <img src={value as string} alt="Hotel" className="w-16 h-10 object-cover rounded" /> : null
  },
  { key: 'destination_id', label: 'Điểm Đến' },
  {
    key: 'star_rating',
    label: 'Hạng Sao',
    render: (value) => `${'⭐'.repeat(Number(value) || 0)}`,
  },
  { key: 'price_range', label: 'Khoảng Giá' },
  {
    key: 'rating',
    label: 'Đánh Giá',
    render: (value) => `${value}/5`,
  },
];

export default function HotelsPage() {
  const { data, isLoading, error, fetchData, createItem, updateItem, deleteItem } =
    useAdminCRUD<Hotel>({ endpoint: 'hotels' });

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Hotel | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleAdd = () => {
    setEditingItem(null);
    setSubmitError(null);
    setIsDialogOpen(true);
  };

  const handleEdit = (item: Hotel) => {
    setEditingItem(item);
    setSubmitError(null);
    setIsDialogOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Bạn có chắc chắn muốn xóa khách sạn này không?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Xóa khách sạn thất bại');
    }
    setDeletingId(null);
  };

  const handleSubmit = async (formData: HotelFormData) => {
    try {
      setIsSubmitting(true);
      setSubmitError(null);

      const amenities = formData.amenities
        ? formData.amenities.split(',').map((a) => a.trim())
        : [];

      if (editingItem) {
        await updateItem(editingItem.id, { ...formData, amenities });
      } else {
        await createItem({ ...formData, amenities });
      }

      setIsDialogOpen(false);
      setEditingItem(null);
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : 'Lưu thất bại');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formFields = [
    {
      name: 'name',
      label: 'Tên Khách Sạn',
      placeholder: 'ví dụ: Grand Hotel Paris',
      required: true,
    },
    {
      name: 'destination_id',
      label: 'ID Điểm Đến',
      placeholder: 'ID điểm đến của khách sạn',
      required: true,
    },
    {
      name: 'star_rating',
      label: 'Hạng Sao (1-5)',
      type: 'number' as const,
      placeholder: '4',
      required: true,
    },
    {
      name: 'price_range',
      label: 'Khoảng Giá',
      placeholder: '$$$',
      required: true,
    },
    {
      name: 'rating',
      label: 'Đánh Giá (0-5)',
      type: 'number' as const,
      placeholder: '4.5',
      required: true,
    },
    {
      name: 'amenities',
      label: 'Tiện Nghi (phân cách bằng dấu phẩy)',
      type: 'textarea' as const,
      placeholder: 'WiFi, Hồ bơi, Gym, Nhà hàng',
      required: false,
    },
    {
      name: 'image_url',
      label: 'Hình Ảnh',
      type: 'image' as const,
      required: false,
    },
  ];

  const getDefaultValues = (hotel: Hotel | null) => {
    if (!hotel) return undefined;

    return {
      ...hotel,
      amenities: Array.isArray(hotel.amenities)
        ? hotel.amenities.join(', ')
        : hotel.amenities || '',
    };
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Quản Lý Khách Sạn
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Tạo, xem, cập nhật và xóa các khách sạn
          </p>
        </div>

        <DataTable
          title="Danh Sách Khách Sạn"
          columns={columns}
          data={data}
          isLoading={isLoading}
          error={error}
          onAdd={handleAdd}
          onEdit={handleEdit}
          onDelete={handleDelete}
          isDeleting={deletingId}
        />
      </div>

      {/* Form Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] flex flex-col">
          <DialogHeader>
            <DialogTitle>
              {editingItem ? 'Chỉnh Sửa Khách Sạn' : 'Thêm Khách Sạn Mới'}
            </DialogTitle>
          </DialogHeader>

          <EntityForm
            title=""
            fields={formFields}
            defaultValues={getDefaultValues(editingItem)}
            onSubmit={handleSubmit}
            isLoading={isSubmitting}
            error={submitError}
            onCancel={() => setIsDialogOpen(false)}
            schema={hotelSchema}
          />
        </DialogContent>
      </Dialog>
    </AdminLayout>
  );
}