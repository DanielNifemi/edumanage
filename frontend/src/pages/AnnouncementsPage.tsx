import React, { useEffect, useState, useCallback } from 'react';
import { notificationsAPI, announcementsAPI } from '../lib/api'; 
import { useAuth } from '@/contexts/useAuth'; 
import { Megaphone, AlertCircle, Edit3, Trash2, PlusCircle, Eye, EyeOff } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '../components/ui/card';
import { useToast } from "../components/ui/use-toast";
import { User, Announcement as AnnouncementTypeFromContext, Notification } from '@/contexts/AuthContextTypes'; // Renamed to avoid conflict

// Define the structure of an Announcement, aligning with AuthContextTypes.ts and user.id
interface Announcement {
  id: string; // Changed to string
  title: string;
  content: string;
  author_details?: {
    id: string; // Changed to string
    username: string;
    first_name?: string;
    last_name?: string;
  };
  created_at: string;
  updated_at: string;
  is_published: boolean;
  // Add other fields from AuthContextTypes.Announcement if necessary
  author?: string; // from AuthContextTypes.Announcement
  published_at?: string | null; // from AuthContextTypes.Announcement
}

// Define the structure for creating/updating an Announcement
interface AnnouncementFormData {
  title: string;
  content: string;
  is_published?: boolean;
}

const AnnouncementItem: React.FC<{
  announcement: Announcement;
  onView: (announcement: Announcement) => void;
  onEdit?: (announcement: Announcement) => void;
  onDelete?: (id: string) => void; // Changed id to string
  onTogglePublish?: (id: string, is_published: boolean) => void; // Changed id to string
  isAdminOrAuthor: boolean;
}> = ({ announcement, onView, onEdit, onDelete, onTogglePublish, isAdminOrAuthor }) => {
  const formatTimestamp = (ts: string) => new Date(ts).toLocaleDateString();

  return (
    <Card className="mb-4">
      <CardHeader>
        <CardTitle className="flex items-center">
          <Megaphone className="w-6 h-6 mr-2 text-blue-500" />
          {announcement.title}
        </CardTitle>
        <CardDescription>
          By: {announcement.author_details?.first_name || announcement.author_details?.username || 'Unknown Author'} | Published: {formatTimestamp(announcement.created_at)}
          {announcement.created_at !== announcement.updated_at && ` | Updated: ${formatTimestamp(announcement.updated_at)}`}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {/* Show a snippet or full content based on a flag or length */}
        <p className="truncate">{announcement.content.substring(0, 150)}{announcement.content.length > 150 && '...'}</p>
      </CardContent>
      <CardFooter className="flex justify-between items-center">
        <Button variant="link" onClick={() => onView(announcement)}>Read More</Button>
        {isAdminOrAuthor && onEdit && onDelete && onTogglePublish && (
          <div className="space-x-2">
            <Button variant="outline" size="sm" onClick={() => onTogglePublish(announcement.id, !announcement.is_published)}>
              {announcement.is_published ? <EyeOff className="w-4 h-4 mr-1" /> : <Eye className="w-4 h-4 mr-1" />}
              {announcement.is_published ? 'Unpublish' : 'Publish'}
            </Button>
            <Button variant="outline" size="sm" onClick={() => onEdit(announcement)}>
              <Edit3 className="w-4 h-4 mr-1" /> Edit
            </Button>
            <Button variant="destructive" size="sm" onClick={() => onDelete(announcement.id)}>
              <Trash2 className="w-4 h-4 mr-1" /> Delete
            </Button>
          </div>
        )}
      </CardFooter>
    </Card>
  );
};

const AnnouncementModal: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  announcement: Announcement | null;
}> = ({ isOpen, onClose, announcement }) => {
  if (!isOpen || !announcement) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <Card className="w-full max-w-2xl bg-white dark:bg-gray-800">
        <CardHeader>
          <CardTitle>{announcement.title}</CardTitle>
          <CardDescription>
            By: {announcement.author_details?.first_name || announcement.author_details?.username || 'Unknown Author'} | Created: {new Date(announcement.created_at).toLocaleString()}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="prose dark:prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: announcement.content.replace(/\n/g, '<br />') }} />
        </CardContent>
        <CardFooter>
          <Button onClick={onClose}>Close</Button>
        </CardFooter>
      </Card>
    </div>
  );
};

const AnnouncementFormModal: React.FC<{
    isOpen: boolean;
    onClose: () => void;
    onSubmit: (data: AnnouncementFormData) => void;
    initialData?: Announcement | null;
}> = ({ isOpen, onClose, onSubmit, initialData }) => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [isPublished, setIsPublished] = useState(false);
    const { toast } = useToast();

    useEffect(() => {
        if (initialData) {
            setTitle(initialData.title);
            setContent(initialData.content);
            setIsPublished(initialData.is_published);
        } else {
            setTitle('');
            setContent('');
            setIsPublished(false);
        }
    }, [initialData, isOpen]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!title.trim() || !content.trim()) {
            toast({ title: "Validation Error", description: "Title and content cannot be empty.", variant: "destructive"});
            return;
        }
        onSubmit({ title, content, is_published: isPublished });
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <Card className="w-full max-w-lg bg-white dark:bg-gray-800">
                <CardHeader>
                    <CardTitle>{initialData ? 'Edit Announcement' : 'Create New Announcement'}</CardTitle>
                </CardHeader>
                <form onSubmit={handleSubmit}>
                    <CardContent className="space-y-4">
                        <div>
                            <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Title</label>
                            <input
                                type="text"
                                id="title"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                                required
                            />
                        </div>
                        <div>
                            <label htmlFor="content" className="block text-sm font-medium text-gray-700 dark:text-gray-300">Content (Markdown supported)</label>
                            <textarea
                                id="content"
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                                rows={10}
                                className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                                required
                            />
                        </div>
                        <div className="flex items-center">
                            <input
                                type="checkbox"
                                id="is_published"
                                checked={isPublished}
                                onChange={(e) => setIsPublished(e.target.checked)}
                                className="h-4 w-4 text-indigo-600 border-gray-300 dark:border-gray-600 rounded focus:ring-indigo-500"
                            />
                            <label htmlFor="is_published" className="ml-2 block text-sm text-gray-900 dark:text-gray-100">
                                Publish Immediately
                            </label>
                        </div>
                    </CardContent>
                    <CardFooter className="flex justify-end space-x-2">
                        <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                        <Button type="submit">{initialData ? 'Save Changes' : 'Create Announcement'}</Button>
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
};


const AnnouncementsPage: React.FC = () => {
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedAnnouncement, setSelectedAnnouncement] = useState<Announcement | null>(null);
  const [isViewModalOpen, setIsViewModalOpen] = useState<boolean>(false);
  const [isFormModalOpen, setIsFormModalOpen] = useState<boolean>(false);
  const [editingAnnouncement, setEditingAnnouncement] = useState<Announcement | null>(null);

  const { toast } = useToast();
  const { user } = useAuth(); // user object now has id directly

  const isAdmin = user?.role === 'admin' || user?.role === 'staff'; // Adjust based on your roles

  const fetchAnnouncements = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await announcementsAPI.getAll();
      // API might return data directly or nested under 'results' if paginated
      setAnnouncements(Array.isArray(data) ? data : data.results || []);
    } catch (err) {
      console.error("Error fetching announcements:", err);
      setError('Failed to load announcements. Please try again later.');
      toast({ title: "Error", description: "Could not fetch announcements.", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    fetchAnnouncements();
  }, [fetchAnnouncements]);

  const handleViewAnnouncement = (announcement: Announcement) => {
    setSelectedAnnouncement(announcement);
    setIsViewModalOpen(true);
  };

  const handleOpenCreateForm = () => {
    setEditingAnnouncement(null);
    setIsFormModalOpen(true);
  };

  const handleOpenEditForm = (announcement: Announcement) => {
    setEditingAnnouncement(announcement);
    setIsFormModalOpen(true);
  };

  const handleFormSubmit = async (formData: AnnouncementFormData) => {
    try {
      if (editingAnnouncement) {
        // Ensure editingAnnouncement.id is a number if API expects number, or API is flexible
        await announcementsAPI.update(parseInt(editingAnnouncement.id, 10), formData); // API expects number
        toast({ title: "Success", description: "Announcement updated successfully." });
      } else {
        await announcementsAPI.create(formData);
        toast({ title: "Success", description: "Announcement created successfully." });
      }
      fetchAnnouncements(); // Refresh list
      setIsFormModalOpen(false);
      setEditingAnnouncement(null);
    } catch (err: unknown) { // Changed from any to unknown
      console.error("Error submitting announcement:", err);
      const message = err instanceof Error ? err.message : "Could not save announcement.";
      toast({ title: "Error", description: message, variant: "destructive" });
    }
  };

  const handleDeleteAnnouncement = async (id: string) => { // id is string here
    if (window.confirm('Are you sure you want to delete this announcement?')) {
      try {
        await announcementsAPI.delete(parseInt(id, 10)); // API expects number
        toast({ title: "Success", description: "Announcement deleted successfully." });
        fetchAnnouncements(); // Refresh list
      } catch (err: unknown) { // Changed from any to unknown
        console.error("Error deleting announcement:", err);
        const message = err instanceof Error ? err.message : "Could not delete announcement.";
        toast({ title: "Error", description: message, variant: "destructive" });
      }
    }
  };

  const handleTogglePublish = async (id: string, currentIsPublished: boolean) => { // id is string here
    try {
      if (currentIsPublished) {
        await announcementsAPI.unpublish(parseInt(id, 10)); // API expects number
        toast({ title: "Success", description: "Announcement unpublished." });
      } else {
        await announcementsAPI.publish(parseInt(id, 10)); // API expects number
        toast({ title: "Success", description: "Announcement published." });
      }
      fetchAnnouncements(); // Refresh list
    } catch (err: unknown) { // Changed from any to unknown
      console.error("Error toggling publish state:", err);
      const message = err instanceof Error ? err.message : "Could not update publish state.";
      toast({ title: "Error", description: message, variant: "destructive" });
    }
  };


  if (loading) {
    return <div className="p-4 text-center">Loading announcements...</div>;
  }

  if (error) {
    return (
      <div className="p-4 text-center text-red-500 flex items-center justify-center">
        <AlertCircle className="w-5 h-5 mr-2"/> {error}
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Announcements</h1>
        {isAdmin && (
          <Button onClick={handleOpenCreateForm}>
            <PlusCircle className="w-5 h-5 mr-2" /> Create New
          </Button>
        )}
      </div>

      {announcements.length === 0 ? (
        <p className="text-center text-gray-500 dark:text-gray-400">No announcements available at the moment.</p>
      ) : (
        <div>
          {announcements.map(announcement => (
            <AnnouncementItem
              key={announcement.id}
              announcement={announcement}
              onView={handleViewAnnouncement}
              // Use user.id directly as it's available on the User type
              onEdit={isAdmin || user?.id === announcement.author_details?.id ? handleOpenEditForm : undefined}
              onDelete={isAdmin || user?.id === announcement.author_details?.id ? handleDeleteAnnouncement : undefined}
              onTogglePublish={isAdmin || user?.id === announcement.author_details?.id ? handleTogglePublish : undefined}
              isAdminOrAuthor={isAdmin || user?.id === announcement.author_details?.id}
            />
          ))}
        </div>
      )}

      {isViewModalOpen && <AnnouncementModal isOpen={isViewModalOpen} onClose={() => setIsViewModalOpen(false)} announcement={selectedAnnouncement} />}
      {isFormModalOpen && <AnnouncementFormModal isOpen={isFormModalOpen} onClose={() => setIsFormModalOpen(false)} onSubmit={handleFormSubmit} initialData={editingAnnouncement} />}
    </div>
  );
};

export default AnnouncementsPage;

