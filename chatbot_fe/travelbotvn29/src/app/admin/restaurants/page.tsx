'use client';

import React, { useEffect, useState } from 'react';
import { AdminLayout } from '@/components/admin/AdminLayout';
import { DataTable, ColumnDef } from '@/components/admin/DataTable';
import { EntityForm } from '@/components/admin/EntityForm';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useAdminCRUD } from '@/hooks/useAdminCRUD';
import { Restaurant } from '@/types';
import { z } from 'zod';

const restaurantSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  destination_id: z.string().min(1, 'Destination is required'),
  cuisine_type: z.string().min(2, 'Cuisine type is required'),
  price_range: z.string().min(1, 'Price range is required'),
  rating: z.coerce.number().min(0).max(5, 'Rating must be between 0 and 5'),
  image_url: z.string().url('Must be a valid URL').optional().or(z.literal('')),
});

type RestaurantFormData = z.infer<typeof restaurantSchema>;

const columns: ColumnDef<Restaurant>[] = [
  { key: 'name', label: 'Restaurant Name' },
  { key: 'destination_id', label: 'Destination' },
  { key: 'cuisine_type', label: 'Cuisine Type' },
  { key: 'price_range', label: 'Price Range' },
  {
    key: 'rating',
    label: 'Rating',
    render: (value) => `${value}/5`,
  },
];

export default function RestaurantsPage() {
  const { data, isLoading, error, fetchData, createItem, updateItem, deleteItem } =
    useAdminCRUD<Restaurant>({ endpoint: 'restaurants' });

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Restaurant | null>(null);
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

  const handleEdit = (item: Restaurant) => {
    setEditingItem(item);
    setSubmitError(null);
    setIsDialogOpen(true);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this restaurant?')) return;
    setDeletingId(id);
    const success = await deleteItem(id);
    if (!success) {
      setSubmitError('Failed to delete restaurant');
    }
    setDeletingId(null);
  };

  const handleSubmit = async (formData: RestaurantFormData) => {
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
      name: 'name',
      label: 'Restaurant Name',
      placeholder: 'e.g., La Belle Vie',
      required: true,
    },
    {
      name: 'destination_id',
      label: 'Destination ID',
      placeholder: 'Restaurant destination ID',
      required: true,
    },
    {
      name: 'cuisine_type',
      label: 'Cuisine Type',
      placeholder: 'e.g., French, Italian, Thai',
      required: true,
    },
    {
      name: 'price_range',
      label: 'Price Range',
      placeholder: '$$',
      required: true,
    },
    {
      name: 'rating',
      label: 'Rating (0-5)',
      type: 'number' as const,
      placeholder: '4.5',
      required: true,
    },
    {
      name: 'image_url',
      label: 'Image URL',
      placeholder: 'https://...',
      required: false,
    },
  ];

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Manage Restaurants
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Create, read, update, and delete restaurant listings
          </p>
        </div>

        <DataTable
          title="Restaurants"
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
              {editingItem ? 'Edit Restaurant' : 'Add New Restaurant'}
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
            schema={restaurantSchema}
          />
        </DialogContent>
      </Dialog>
    </AdminLayout>
  );
}
