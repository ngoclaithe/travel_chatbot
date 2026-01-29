'use client';

import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Trash2, Edit2, Plus, AlertCircle, Loader2 } from 'lucide-react';
import { Skeleton } from '@/components/ui/skeleton';

export interface ColumnDef<T> {
  key: keyof T;
  label: string;
  render?: (value: T[keyof T]) => React.ReactNode;
  width?: string;
}

interface DataTableProps<T extends { id: string }> {
  title: string;
  columns: ColumnDef<T>[];
  data: T[];
  isLoading?: boolean;
  error?: string | null;
  onAdd?: () => void;
  onEdit?: (item: T) => void;
  onDelete?: (id: string) => void;
  isDeleting?: string | null;
}

function DataTableInner<T extends { id: string }>(
  {
    title,
    columns,
    data,
    isLoading = false,
    error = null,
    onAdd,
    onEdit,
    onDelete,
    isDeleting = null,
  }: DataTableProps<T>,
  ref: React.ForwardedRef<HTMLDivElement>
) {
  return (
    <Card ref={ref}>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>{title}</CardTitle>
        {onAdd && (
          <Button
            onClick={onAdd}
            className="bg-ocean-blue hover:bg-ocean-dark gap-2"
          >
            <Plus className="w-4 h-4" />
            Add New
          </Button>
        )}
      </CardHeader>

      <CardContent>
        {error && (
          <div className="bg-destructive/10 border border-destructive text-destructive p-4 rounded-lg mb-4 flex items-center gap-3">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {isLoading ? (
          <div className="space-y-2">
            {Array.from({ length: 5 }).map((_, i) => (
              <Skeleton key={i} className="h-12 rounded" />
            ))}
          </div>
        ) : data.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            No data found. {onAdd && 'Click "Add New" to create an entry.'}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  {columns.map((column) => (
                    <TableHead
                      key={String(column.key)}
                      style={{ width: column.width }}
                    >
                      {column.label}
                    </TableHead>
                  ))}
                  <TableHead className="text-right w-24">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.map((item) => (
                  <TableRow key={item.id}>
                    {columns.map((column) => (
                      <TableCell key={String(column.key)}>
                        {column.render
                          ? column.render(item[column.key])
                          : String(item[column.key] || '-')}
                      </TableCell>
                    ))}
                    <TableCell className="text-right space-x-2 flex justify-end gap-2">
                      {onEdit && (
                        <Button
                          variant="outline"
                          size="icon"
                          onClick={() => onEdit(item)}
                          disabled={isDeleting === item.id}
                        >
                          <Edit2 className="w-4 h-4" />
                        </Button>
                      )}
                      {onDelete && (
                        <Button
                          variant="outline"
                          size="icon"
                          onClick={() => onDelete(item.id)}
                          disabled={isDeleting === item.id}
                        >
                          {isDeleting === item.id ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                          ) : (
                            <Trash2 className="w-4 h-4 text-destructive" />
                          )}
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export const DataTable = React.forwardRef(DataTableInner) as <T extends { id: string }>(
  props: DataTableProps<T> & { ref?: React.ForwardedRef<HTMLDivElement> }
) => ReturnType<typeof DataTableInner>;