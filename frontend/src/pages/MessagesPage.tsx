import React, { useEffect, useState, useCallback } from 'react';
import { communicationAPI, ReceivedMessageData as ApiReceivedMessageData, UserBasicData } from '@/lib/api';
import { useAuth } from '@/contexts/useAuth';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { MessageSquare, AlertTriangle, Send, Inbox, SendHorizontal, UserCircle } from 'lucide-react';
import { NewMessageDialog } from '@/components/messages/NewMessageDialog';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

// Define PaginatedResponse interface
interface PaginatedResponse<T> {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results: T[];
}

interface DisplayMessageData {
  id: string | number;
  sender?: UserBasicData;
  recipient?: UserBasicData;
  sender_name?: string;
  recipient_name?: string;
  subject: string;
  content: string;
  timestamp: string;
  is_read: boolean;
  // For displaying the relevant person in the list (sender for inbox, recipient for sent)
  relevant_user_name?: string;
  relevant_user_avatar_seed?: string; // For generating consistent avatar placeholders
}

const MessagesPage: React.FC = () => {
  const { user } = useAuth();
  const [inboxMessages, setInboxMessages] = useState<DisplayMessageData[]>([]);
  const [sentMessages, setSentMessages] = useState<DisplayMessageData[]>([]);
  const [loadingInbox, setLoadingInbox] = useState<boolean>(true);
  const [loadingSent, setLoadingSent] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isNewMessageDialogOpen, setIsNewMessageDialogOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<'inbox' | 'sent'>('inbox');

  const formatMessages = (
    messagesInput: ApiReceivedMessageData[] | PaginatedResponse<ApiReceivedMessageData>, // Changed parameter name and type
    messageType: 'inbox' | 'sent'
  ): DisplayMessageData[] => {
    const actualMessagesArray: ApiReceivedMessageData[] = Array.isArray(messagesInput)
      ? messagesInput
      : (messagesInput && typeof messagesInput === 'object' && Array.isArray(messagesInput.results))
        ? messagesInput.results
        : [];

    return actualMessagesArray.map(msg => ({
      id: msg.id,
      sender: msg.sender,
      recipient: msg.recipient,
      sender_name: msg.sender?.username || msg.sender_name || 'Unknown Sender',
      recipient_name: msg.recipient?.username || 'Unknown Recipient',
      subject: msg.subject,
      content: msg.body || '', // Corrected: use msg.body as per ReceivedMessageData
      timestamp: msg.created_at || new Date().toISOString(), // Corrected: use msg.created_at
      is_read: msg.is_read || false,
      relevant_user_name: messageType === 'inbox' 
        ? (msg.sender?.full_name || msg.sender?.username || 'Unknown Sender') 
        : (msg.recipient?.full_name || msg.recipient?.username || 'Unknown Recipient'),
      relevant_user_avatar_seed: messageType === 'inbox' 
        ? (msg.sender?.username || String(msg.sender?.id))
        : (msg.recipient?.username || String(msg.recipient?.id)),
    }));
  };

  const fetchInboxMessages = useCallback(async () => {
    setLoadingInbox(true);
    setError(null);
    try {
      const messagesFromApi = await communicationAPI.getInboxMessages();
      setInboxMessages(formatMessages(messagesFromApi, 'inbox'));
    } catch (err) {
      console.error("Error fetching inbox messages:", err);
      setError('Failed to load inbox messages. Please try again later.');
    } finally {
      setLoadingInbox(false);
    }
  }, []);

  const fetchSentMessages = useCallback(async () => {
    setLoadingSent(true);
    setError(null);
    try {
      const messagesFromApi = await communicationAPI.getSentMessages();
      setSentMessages(formatMessages(messagesFromApi, 'sent'));
    } catch (err) {
      console.error("Error fetching sent messages:", err);
      setError('Failed to load sent messages. Please try again later.');
    } finally {
      setLoadingSent(false);
    }
  }, []);

  useEffect(() => {
    if (activeTab === 'inbox') {
      fetchInboxMessages();
    } else if (activeTab === 'sent') {
      fetchSentMessages();
    }
  }, [activeTab, fetchInboxMessages, fetchSentMessages]);

  const handleNewMessageSent = () => {
    if (activeTab === 'inbox') {
      fetchInboxMessages(); 
    } else {
      fetchSentMessages();
    }
    // Potentially switch to sent tab after sending a message
    // setActiveTab('sent'); 
  };

  const renderMessageList = (messagesToList: DisplayMessageData[], type: 'inbox' | 'sent') => {
    if ((type === 'inbox' && loadingInbox) || (type === 'sent' && loadingSent)) {
      return <div className="p-6 text-center">Loading messages...</div>;
    }
    if (error && ((type === 'inbox' && messagesToList.length === 0) || (type === 'sent' && messagesToList.length === 0))) {
        return (
          <div className="p-6">
            <Alert variant="destructive" className="mb-4">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
            <Button onClick={type === 'inbox' ? fetchInboxMessages : fetchSentMessages}>Try Again</Button>
          </div>
        );
      }
    if (messagesToList.length === 0) {
      return (
        <Card className="text-center mt-4">
          <CardHeader>
            <CardTitle>No Messages</CardTitle>
          </CardHeader>
          <CardContent>
            <MessageSquare className="h-12 w-12 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 dark:text-gray-400">You have no {type} messages.</p>
          </CardContent>
        </Card>
      );
    }

    return (
      <div className="space-y-4 mt-4">
        {messagesToList.map(msg => (
          <Card key={msg.id} className={`${!msg.is_read && type === 'inbox' ? 'border-blue-500 border-2' : ''} hover:shadow-lg transition-shadow`}>
            <CardHeader className="flex flex-row items-start gap-4 space-y-0 pb-3">
                <Avatar className="h-10 w-10 border">
                    <AvatarImage src={`https://api.dicebear.com/8.x/initials/svg?seed=${msg.relevant_user_avatar_seed}`} alt={msg.relevant_user_name} />
                    <AvatarFallback><UserCircle size={24}/></AvatarFallback>
                </Avatar>
                <div className="flex-1">
                    <CardTitle className="text-lg mb-0.5">{msg.subject}</CardTitle>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                    {type === 'inbox' ? `From: ` : `To: `}
                    <Button variant="link" className="p-0 h-auto text-xs text-blue-600 hover:underline" onClick={() => alert(`Show profile for ${msg.relevant_user_name}`)}>
                        {msg.relevant_user_name}
                    </Button>
                    {' | '} {new Date(msg.timestamp).toLocaleString()}
                    </p>
                </div>
                {type === 'inbox' && !msg.is_read && (
                    <div className="w-3 h-3 bg-blue-500 rounded-full mt-1" title="Unread"></div>
                )}
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">
                {msg.content}
              </p>
            </CardContent>
            {/* Optional: Add CardFooter for actions like Reply, Delete, etc. */}
            {/* <CardFooter className="flex justify-end gap-2">
              <Button variant="outline" size="sm">Reply</Button>
            </CardFooter> */}
          </Card>
        ))}
      </div>
    );
  };

  return (
    <div className="p-4 md:p-6">
      <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Messages</h1>
        <Button onClick={() => setIsNewMessageDialogOpen(true)} className="w-full sm:w-auto">
          <Send className="h-4 w-4 mr-2" />
          New Message
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as 'inbox' | 'sent')} className="w-full">
        <TabsList className="grid w-full grid-cols-2 sm:w-[400px]">
          <TabsTrigger value="inbox">
            <Inbox className="h-4 w-4 mr-2" /> Inbox
          </TabsTrigger>
          <TabsTrigger value="sent">
            <SendHorizontal className="h-4 w-4 mr-2" /> Sent
          </TabsTrigger>
        </TabsList>
        <TabsContent value="inbox">
          {renderMessageList(inboxMessages, 'inbox')}
        </TabsContent>
        <TabsContent value="sent">
          {renderMessageList(sentMessages, 'sent')}
        </TabsContent>
      </Tabs>

      {error && (inboxMessages.length > 0 || sentMessages.length > 0) && (
         <Alert variant="destructive" className="mt-6">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
      )}

      <NewMessageDialog
        open={isNewMessageDialogOpen}
        onOpenChange={setIsNewMessageDialogOpen}
        onMessageSent={handleNewMessageSent}
      />
    </div>
  );
};

export default MessagesPage;
