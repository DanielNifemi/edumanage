import React, { useEffect, useState, useCallback } from 'react';
import { notificationsAPI } from '../lib/api';
import { Bell, CheckCircle, XCircle } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { useToast } from "../components/ui/use-toast";
import { useAuth } from '../contexts/useAuth'; // Import useAuth

interface Notification {
  id: number;
  notification_type: string;
  text_content: string;
  timestamp: string;
  is_read: boolean;
  // Add other relevant fields from your Notification model if needed
  // e.g., related_object_id, message_details, etc.
}

const NotificationItem: React.FC<{ notification: Notification; onMarkAsRead: (id: number) => void }> = ({ notification, onMarkAsRead }) => {
  const formatTimestamp = (ts: string) => {
    return new Date(ts).toLocaleString();
  };

  return (
    <div className={`p-4 mb-2 border rounded-lg ${notification.is_read ? 'bg-gray-100 dark:bg-gray-800' : 'bg-white dark:bg-gray-700'} flex items-start`}>
      <div className="flex-shrink-0 mr-3">
        <Bell className={`w-6 h-6 ${notification.is_read ? 'text-gray-400' : 'text-blue-500'}`} />
      </div>
      <div className="flex-grow">
        <p className={`font-semibold ${notification.is_read ? 'text-gray-600 dark:text-gray-400' : 'text-gray-900 dark:text-white'}`}>
          {notification.notification_type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
        </p>
        <p className={`text-sm ${notification.is_read ? 'text-gray-500 dark:text-gray-400' : 'text-gray-700 dark:text-gray-300'}`}>
          {notification.text_content}
        </p>
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
          {formatTimestamp(notification.timestamp)}
        </p>
      </div>
      {!notification.is_read && (
        <Button variant="ghost" size="sm" onClick={() => onMarkAsRead(notification.id)} className="ml-auto">
          <CheckCircle className="w-5 h-5 text-green-500 mr-1" /> Mark as Read
        </Button>
      )}
    </div>
  );
};

const NotificationsPage: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();
  const { refreshUnreadCount } = useAuth(); // Get refreshUnreadCount from AuthContext

  const fetchNotifications = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await notificationsAPI.getAll();
      // Assuming the API returns a list of notifications directly or under a 'results' key for paginated responses
      setNotifications(Array.isArray(data) ? data : data.results || []);
    } catch (err) {
      console.error("Error fetching notifications:", err);
      setError('Failed to load notifications. Please try again later.');
      toast({
        title: "Error",
        description: "Could not fetch notifications.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    fetchNotifications();
  }, [fetchNotifications]);

  const handleMarkAsRead = async (id: number) => {
    try {
      await notificationsAPI.markAsRead(id);
      setNotifications(prevNotifications =>
        prevNotifications.map(n => (n.id === id ? { ...n, is_read: true } : n))
      );
      await refreshUnreadCount(); // Refresh global unread count
      toast({
        title: "Success",
        description: "Notification marked as read.",
      });
    } catch (err) {
      console.error("Error marking notification as read:", err);
      toast({
        title: "Error",
        description: "Could not mark notification as read.",
        variant: "destructive",
      });
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await notificationsAPI.markAllAsRead();
      fetchNotifications(); // Refetch to get updated list for the page
      await refreshUnreadCount(); // Refresh global unread count
      toast({
        title: "Success",
        description: "All notifications marked as read.",
      });
    } catch (err) {
      console.error("Error marking all notifications as read:", err);
      toast({
        title: "Error",
        description: "Could not mark all notifications as read.",
        variant: "destructive",
      });
    }
  };
  
  const unreadCount = notifications.filter(n => !n.is_read).length;

  if (loading) {
    return <div className="p-4 text-center">Loading notifications...</div>;
  }

  if (error) {
    return (
      <div className="p-4 text-center text-red-500 flex items-center justify-center">
        <XCircle className="w-5 h-5 mr-2"/> {error}
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-2xl font-bold">Notifications</CardTitle>
          {notifications.length > 0 && unreadCount > 0 && (
             <Button onClick={handleMarkAllAsRead} variant="outline">
                Mark All as Read ({unreadCount})
            </Button>
          )}
        </CardHeader>
        <CardContent>
          {notifications.length === 0 ? (
            <p className="text-center text-gray-500 dark:text-gray-400">You have no notifications.</p>
          ) : (
            <div>
              {notifications.map(notification => (
                <NotificationItem
                  key={notification.id}
                  notification={notification}
                  onMarkAsRead={handleMarkAsRead}
                />
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default NotificationsPage;
