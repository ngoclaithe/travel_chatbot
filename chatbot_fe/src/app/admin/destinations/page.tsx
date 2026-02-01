'use client';

import React, { useEffect, useState } from 'react';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { DataTable, ColumnDef } from '@/components/admin/DataTable';
import { EntityForm } from '@/components/admin/EntityForm';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useAdminCRUD } from '@/hooks/useAdminCRUD';
import { Destination } from '@/types';
import { z } from 'zod';

const destinationSchema = z.object({
  name: z.string().min(2, 'Tên phải có ít nhất 2 ký tự'),
  province: z.string().min(2, 'Tỉnh/Thành Phố là bắt buộc'),
  region: z.string().min(2, 'Khu Vực là bắt buộc'),
  rating: z.coerce.number().min(0).max(5, 'Đánh giá phải từ 0 đến 5'),
  best_time_to_visit: z.string().min(2, 'Thời gian tốt nhất là bắt buộc'),
  description: z.string().min(10, 'Mô tả phải có ít nhất 10 ký tự'),
  image_url: z.string().url('Phải là một URL hợp lệ').optional().or(z.literal('')),
});

type DestinationFormData = z.infer<typeof destinationSchema>;

const columns: ColumnDef<Destination>[] = [
  { key: 'name', label: 'Tên' },
  {
    key: 'image_url',
    label: 'Hình Ảnh',
    render: (value) => value ? <img src={value as string} alt="Dest" className="w-16 h-10 object-cover rounded" /> : null
  },
  { key: 'province', label: 'Tỉnh/Thành Phố' },
  { key: 'region', label: 'Khu Vực' },
  {
    key: 'rating',
    label: 'Đánh Giá',
    render: (value) => `${value}/5`,
  },
  { key: 'best_time_to_visit', label: 'Thời Gian Tốt Nhất' },
];

export default function DestinationsPage() {
  // ... (existing code stays same until return)
  const { data, isLoading, error, fetchData, createItem, updateItem, deleteItem } =
    useAdminCRUD<Destination>({ endpoint: 'destinations' });

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Destination | null>(null);
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

  const handleEdit = (item: Destination) => {
    setEditingItem(item);
    setSubmitError(null);
    setIsDialogOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Bạn có chắc chắn muốn xóa điểm đến này?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Xóa điểm đến thất bại');
    }
    setDeletingId(null);
  };

  const handleSubmit = async (formData: DestinationFormData) => {
    try {
      setIsSubmitting(true);
      setSubmitError(null);

      if (editingItem) {
        await updateItem(editingItem.id, formData);
      } else {
        await createItem(formData);
      }

      setIsDialogOpen(false);
      setEditingItem(null);
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : 'Không thể lưu');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formFields = [
    {
      name: 'name',
      label: 'Tên Điểm Đến',
      placeholder: 'ví dụ: Paris, Tokyo',
      required: true,
    },
    {
      name: 'province',
      label: 'Tỉnh/Thành Phố',
      placeholder: 'ví dụ: Île-de-France',
      required: true,
    },
    {
      name: 'region',
      label: 'Khu Vực',
      placeholder: 'ví dụ: Châu Âu, Châu Á',
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
      name: 'best_time_to_visit',
      label: 'Thời Gian Tốt Nhất Để Thăm',
      placeholder: 'ví dụ: Tháng 4 đến Tháng 5',
      required: true,
    },
    {
      name: 'description',
      label: 'Mô Tả',
      type: 'textarea' as const,
      placeholder: 'Mô tả điểm đến này...',
      required: true,
    },
    {
      name: 'image_url',
      label: 'Hình Ảnh',
      type: 'image' as const,
      required: false,
    },
  ];

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Quản Lý Điểm Đến
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Tạo, đọc, cập nhật và xóa các điểm đến du lịch
          </p>
        </div>

        <DataTable
          title="Danh Sách Điểm Đến"
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
              {editingItem ? 'Chỉnh Sửa Điểm Đến' : 'Thêm Điểm Đến Mới'}
            </DialogTitle>
          </DialogHeader>

          <EntityForm
            title=""
            fields={formFields}
            defaultValues={editingItem || undefined}
            onSubmit={handleSubmit}
            isLoading={isSubmitting}
            error={submitError}
            onCancel={() => setIsDialogOpen(false)}
            schema={destinationSchema}
          />
        </DialogContent>
      </Dialog>
    </AdminLayout>
  );
}
