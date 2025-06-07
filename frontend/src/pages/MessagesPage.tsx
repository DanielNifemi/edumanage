import React, { useEffect, useState, useCallback } from 'react';
import { communicationAPI } from '@/lib/api'; // Import communicationAPI
import { useAuth } from '@/contexts/useAuth';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { MessageSquare, AlertTriangle, Send } from 'lucide-react';

// This interface is for displaying received messages.
// If api.ts exports a specific type for received messages, consider using/aligning with that.
interface ReceivedMessageData {
  id: string; // Or number, depending on backend
  sender_name?: string; // Backend might send sender_id, requiring a lookup or join
  subject: string;
  content: string; // Changed from snippet to content for clarity
  timestamp: string;
  is_read: boolean;
  // Add other relevant fields from the backend API response for messages
}

const MessagesPage: React.FC = () => {
  const { user } = useAuth(); // user might be needed for context or future features
  const [messages, setMessages] = useState<ReceivedMessageData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMessages = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      // Replace with actual API call
      const data = await communicationAPI.getMessages();
      // Ensure data is an array, or adapt if the API returns a paginated response (e.g., data.results)
      // Also, map the received data to ReceivedMessageData if necessary
      const formattedMessages = (Array.isArray(data) ? data : (data.results || [])).map(msg => ({
        id: msg.id,
        sender_name: msg.sender?.username || msg.sender_name || 'Unknown Sender', // Adjust based on actual sender data structure
        subject: msg.subject,
        content: msg.content || msg.body || '', // Adjust based on actual content field name
        timestamp: msg.timestamp || msg.created_at,
        is_read: msg.is_read || false,
      }));
      setMessages(formattedMessages);
    } catch (err) {
      console.error("Error fetching messages:", err);
      setError('Failed to load messages. Please try again later.');
    } finally {
      setLoading(false);
    }
  }, []); // Removed user from dependency array as it's not directly used in this fetchMessages

  useEffect(() => {
    fetchMessages();
  }, [fetchMessages]);

  if (loading) {
    return <div className="p-6 text-center">Loading messages...</div>;
  }

  if (error) {
    return (
      <div className="p-6">
        <Alert variant="destructive" className="mb-4">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
        <Button onClick={fetchMessages}>Try Again</Button>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Messages</h1>
        <Button>
          <Send className="h-4 w-4 mr-2" />
          New Message
        </Button>
      </div>

      {messages.length === 0 ? (
        <Card className="text-center">
          <CardHeader>
            <CardTitle>No Messages</CardTitle>
          </CardHeader>
          <CardContent>
            <MessageSquare className="h-12 w-12 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 dark:text-gray-400">You have no messages in your inbox.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {messages.map(msg => (
            <Card key={msg.id} className={!msg.is_read ? 'border-blue-500' : ''}>
              <CardHeader>
                <CardTitle className="text-lg">{msg.subject}</CardTitle>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  From: {msg.sender_name} | Received: {new Date(msg.timestamp).toLocaleString()}
                </p>
              </CardHeader>
              <CardContent>
                {/* <p className="text-sm text-gray-700 dark:text-gray-300">{msg.snippet}</p> */}
                <p className="text-sm text-gray-700 dark:text-gray-300">{msg.content}</p>
              </CardContent>
              {/* Add CardFooter for actions like Reply, Delete, Mark as Unread */}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default MessagesPage;
