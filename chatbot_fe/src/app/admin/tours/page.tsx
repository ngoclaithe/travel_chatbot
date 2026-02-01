'use client';

import React, { useEffect, useState } from 'react';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { DataTable, ColumnDef } from '@/components/admin/DataTable';
import { EntityForm } from '@/components/admin/EntityForm';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useAdminCRUD } from '@/hooks/useAdminCRUD';
import { Tour } from '@/types';
import { z } from 'zod';

const tourSchema = z.object({
  name: z.string().min(2, 'Tên phải có ít nhất 2 ký tự'),
  destinations: z.string().min(1, 'Điểm đến là bắt buộc'),
  duration_days: z.coerce.number().min(1, 'Thời gian phải ít nhất 1 ngày'),
  price: z.coerce.number().min(0, 'Giá phải là số dương'),
  description: z.string().min(10, 'Mô tả phải có ít nhất 10 ký tự'),
  image_url: z.string().url('Phải là một URL hợp lệ').optional().or(z.literal('')),
});

type TourFormData = z.infer<typeof tourSchema>;

const columns: ColumnDef<Tour>[] = [
  { key: 'name', label: 'Tên Tour' },
  {
    key: 'destinations',
    label: 'Điểm Đến',
    render: (value) => {
      if (!value) return '';
      let processed = value;
      if (typeof value === 'string') {
        try {
          if (value.trim().startsWith('[') || value.trim().startsWith('{')) {
            processed = JSON.parse(value);
          }
        } catch { }
      }

      if (Array.isArray(processed)) {
        return processed.map((item: any) => {
          let finalItem = item;
          if (typeof item === 'string' && (item.trim().startsWith('[') || item.trim().startsWith('{'))) {
            try {
              const parsed = JSON.parse(item);
              if (Array.isArray(parsed)) {
                return parsed.map((kp: any) => kp.name || kp.title || kp).join(', ');
              }
              if (typeof parsed === 'object' && parsed !== null) {
                finalItem = parsed;
              }
            } catch { }
          }

          if (typeof finalItem === 'object' && finalItem !== null) {
            return finalItem.name || finalItem.title || JSON.stringify(finalItem);
          }
          return String(finalItem);
        }).join(', ');
      }
      return String(value);
    },
  },
  {
    key: 'duration_days',
    label: 'Thời Lượng',
    render: (value) => `${value} ngày`,
  },
  {
    key: 'price',
    label: 'Giá',
    render: (value) => `${Number(value).toLocaleString('vi-VN')} VNĐ`,
  },
];

export default function ToursPage() {
  const { data, isLoading, error, fetchData, createItem, updateItem, deleteItem } =
    useAdminCRUD<Tour>({ endpoint: 'tours' });

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Tour | null>(null);
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

  const handleEdit = (item: Tour) => {
    setEditingItem(item);
    setSubmitError(null);
    setIsDialogOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Bạn có chắc chắn muốn xóa tour này không?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Xóa tour thất bại');
    }
    setDeletingId(null);
  };

  const handleSubmit = async (formData: TourFormData) => {
    try {
      setIsSubmitting(true);
      setSubmitError(null);

      const destinations = formData.destinations
        .split(',')
        .map((d) => d.trim());

      if (editingItem) {
        await updateItem(editingItem.id, { ...formData, destinations });
      } else {
        await createItem({ ...formData, destinations });
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
      label: 'Tên Tour',
      placeholder: 'ví dụ: Tour Khám Phá Đông Nam Á',
      required: true,
    },
    {
      name: 'destinations',
      label: 'Điểm Đến (phân cách bằng dấu phẩy)',
      type: 'textarea' as const,
      placeholder: 'Bangkok, Phuket, Ho Chi Minh',
      required: true,
    },
    {
      name: 'duration_days',
      label: 'Thời Lượng (ngày)',
      type: 'number' as const,
      placeholder: '7',
      required: true,
    },
    {
      name: 'price',
      label: 'Giá mỗi người',
      type: 'number' as const,
      placeholder: '1200000',
      required: true,
    },
    {
      name: 'description',
      label: 'Mô Tả',
      type: 'textarea' as const,
      placeholder: 'Mô tả chi tiết về tour...',
      required: true,
    },
    {
      name: 'image_url',
      label: 'Hình Ảnh',
      type: 'image' as const,
      required: false,
    },
  ];

  const getDefaultValues = (tour: Tour | null) => {
    if (!tour) return undefined;

    return {
      ...tour,
      destinations: Array.isArray(tour.destinations)
        ? tour.destinations.join(', ')
        : typeof tour.destinations === 'string'
          ? tour.destinations
          : '',
    };
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Quản Lý Tour
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Tạo, xem, cập nhật và xóa các gói tour du lịch
          </p>
        </div>

        <DataTable
          title="Danh Sách Tour"
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
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingItem ? 'Chỉnh Sửa Tour' : 'Thêm Tour Mới'}
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
            schema={tourSchema}
          />
        </DialogContent>
      </Dialog>
    </AdminLayout>
  );
}