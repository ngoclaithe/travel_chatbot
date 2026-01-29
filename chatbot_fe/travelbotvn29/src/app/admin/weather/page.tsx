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
  destination_id: z.string().min(1, 'Destination is required'),
  month: z.coerce.number().min(1).max(12, 'Month must be between 1 and 12'),
  avg_temp: z.coerce.number().min(-50).max(60, 'Temperature must be realistic'),
  description: z.string().min(5, 'Description is required'),
  is_best_time: z.boolean().default(false),
});

type WeatherFormData = z.infer<typeof weatherSchema>;

const columns: ColumnDef<Weather>[] = [
  { key: 'destination_id', label: 'Destination' },
  {
    key: 'month',
    label: 'Month',
    render: (value) => {
      const monthNum = Number(value);
      if (!monthNum || monthNum < 1 || monthNum > 12) return String(value);
      return new Date(2024, monthNum - 1).toLocaleDateString('en-US', { month: 'long' });
    },
  },
  {
    key: 'avg_temp',
    label: 'Avg Temp',
    render: (value) => `${value}°C`,
  },
  {
    key: 'is_best_time',
    label: 'Best Time',
    render: (value) => (value ? '✓ Yes' : 'No'),
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
    if (!confirm('Are you sure?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Failed to delete');
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
      setSubmitError(err instanceof Error ? err.message : 'Failed to save');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formFields = [
    {
      name: 'destination_id',
      label: 'Destination ID',
      placeholder: 'Destination ID',
      required: true,
    },
    {
      name: 'month',
      label: 'Month (1-12)',
      type: 'number' as const,
      placeholder: '1',
      required: true,
    },
    {
      name: 'avg_temp',
      label: 'Average Temperature (°C)',
      type: 'number' as const,
      placeholder: '25',
      required: true,
    },
    {
      name: 'description',
      label: 'Weather Description',
      type: 'textarea' as const,
      placeholder: 'Sunny and warm...',
      required: true,
    },
    {
      name: 'is_best_time',
      label: 'Best Time to Visit',
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
            Manage Weather
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Weather information by destination and month
          </p>
        </div>

        <DataTable
          title="Weather Data"
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
              {editingItem ? 'Edit Weather' : 'Add Weather Data'}
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
