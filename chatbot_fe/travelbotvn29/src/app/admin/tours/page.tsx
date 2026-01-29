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
  name: z.string().min(2, 'Name must be at least 2 characters'),
  destinations: z.string().min(1, 'Destinations are required'),
  duration_days: z.coerce.number().min(1, 'Duration must be at least 1 day'),
  price: z.coerce.number().min(0, 'Price must be positive'),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  image_url: z.string().url('Must be a valid URL').optional().or(z.literal('')),
});

type TourFormData = z.infer<typeof tourSchema>;

const columns: ColumnDef<Tour>[] = [
  { key: 'name', label: 'Tour Name' },
  {
    key: 'destinations',
    label: 'Destinations',
    render: (value) => Array.isArray(value) ? value.join(', ') : String(value),
  },
  {
    key: 'duration_days',
    label: 'Duration',
    render: (value) => `${value} days`,
  },
  {
    key: 'price',
    label: 'Price',
    render: (value) => `$${value}`,
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
    if (!confirm('Are you sure you want to delete this tour?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Failed to delete tour');
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
      setSubmitError(err instanceof Error ? err.message : 'Failed to save');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formFields = [
    {
      name: 'name',
      label: 'Tour Name',
      placeholder: 'e.g., Southeast Asia Explorer',
      required: true,
    },
    {
      name: 'destinations',
      label: 'Destinations (comma separated)',
      type: 'textarea' as const,
      placeholder: 'Bangkok, Phuket, Ho Chi Minh',
      required: true,
    },
    {
      name: 'duration_days',
      label: 'Duration (days)',
      type: 'number' as const,
      placeholder: '7',
      required: true,
    },
    {
      name: 'price',
      label: 'Price per person',
      type: 'number' as const,
      placeholder: '1200',
      required: true,
    },
    {
      name: 'description',
      label: 'Description',
      type: 'textarea' as const,
      placeholder: 'Describe this tour...',
      required: true,
    },
    {
      name: 'image_url',
      label: 'Image URL',
      placeholder: 'https://...',
      required: false,
    },
  ];

  const getDefaultValues = (tour: Tour | null) => {
    if (!tour) return undefined;
    
    return {
      ...tour,
      destinations: Array.isArray(tour.destinations) 
        ? tour.destinations.join(', ')  
        : tour.destinations || '',
    };
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Manage Tours
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Create, read, update, and delete tour packages
          </p>
        </div>

        <DataTable
          title="Tours"
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
              {editingItem ? 'Edit Tour' : 'Add New Tour'}
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