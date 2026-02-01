'use client';

import React, { useEffect, useState } from 'react';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { DataTable, ColumnDef } from '@/components/admin/DataTable';
import { EntityForm } from '@/components/admin/EntityForm';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useAdminCRUD } from '@/hooks/useAdminCRUD';
import { Weather } from '@/types';
import { z } from 'zod';

const weatherSchema = z.object({
  destination_id: z.string().min(1, 'Điểm đến là bắt buộc'),
  month: z.coerce.number().min(1).max(12, 'Tháng phải từ 1 đến 12'),
  avg_temp: z.coerce.number().min(-50).max(60, 'Nhiệt độ không hợp lệ'),
  description: z.string().min(5, 'Mô tả là bắt buộc'),
  is_best_time: z.boolean().default(false),
});

type WeatherFormData = z.infer<typeof weatherSchema>;

const columns: ColumnDef<Weather>[] = [
  { key: 'destination_id', label: 'Điểm Đến' },
  {
    key: 'month',
    label: 'Tháng',
    render: (value) => {
      const monthNum = Number(value);
      if (!monthNum || monthNum < 1 || monthNum > 12) return String(value);
      return `Tháng ${monthNum}`;
    },
  },
  {
    key: 'avg_temp',
    label: 'Nhiệt Độ TB',
    render: (value) => `${value}°C`,
  },
  {
    key: 'is_best_time',
    label: 'Thời Điểm Tốt Nhất',
    render: (value) => (value ? '✓ Có' : 'Không'),
  },
];

export default function WeatherPage() {
  const { data, isLoading, error, fetchData, createItem, updateItem, deleteItem } =
    useAdminCRUD<Weather>({ endpoint: 'weather' });

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Weather | null>(null);
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

  const handleEdit = (item: Weather) => {
    setEditingItem(item);
    setSubmitError(null);
    setIsDialogOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Bạn có chắc chắn muốn xóa không?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Xóa thất bại');
    }
    setDeletingId(null);
  };

  const handleSubmit = async (formData: WeatherFormData) => {
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
      setSubmitError(err instanceof Error ? err.message : 'Lưu thất bại');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formFields = [
    {
      name: 'destination_id',
      label: 'ID Điểm Đến',
      placeholder: 'ID Điểm Đến',
      required: true,
    },
    {
      name: 'month',
      label: 'Tháng (1-12)',
      type: 'number' as const,
      placeholder: '1',
      required: true,
    },
    {
      name: 'avg_temp',
      label: 'Nhiệt Độ Trung Bình (°C)',
      type: 'number' as const,
      placeholder: '25',
      required: true,
    },
    {
      name: 'description',
      label: 'Mô Tả Thời Tiết',
      type: 'textarea' as const,
      placeholder: 'Nắng ấm...',
      required: true,
    },
    {
      name: 'is_best_time',
      label: 'Thời Điểm Tốt Nhất Để Thăm',
      type: 'checkbox' as const,
    },
  ];

  const getDefaultValues = (weather: Weather | null): Partial<WeatherFormData> | undefined => {
    if (!weather) return undefined;

    return {
      destination_id: weather.destination_id,
      month: weather.month,
      avg_temp: weather.avg_temp,
      description: weather.description,
      is_best_time: weather.is_best_time,
    };
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Quản Lý Thời Tiết
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Thông tin thời tiết theo điểm đến và tháng
          </p>
        </div>

        <DataTable
          title="Danh Sách Thời Tiết"
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

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingItem ? 'Chỉnh Sửa Thời Tiết' : 'Thêm Dữ Liệu Thời Tiết'}
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
            schema={weatherSchema}
          />
        </DialogContent>
      </Dialog>
    </AdminLayout>
  );
}
