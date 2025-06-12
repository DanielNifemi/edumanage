// filepath: c:\Users\USER\PycharmProjects\edumanage\frontend\src\components\messages\NewMessageDialog.tsx
import React, { useState, useEffect, useCallback } from 'react';
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogClose, // DialogTrigger is not used directly here, Dialog controls open state via props
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { accountsAPI, communicationAPI, UserBasicData, SentMessageData } from '@/lib/api';
import { useAuth } from '@/contexts/useAuth';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertTriangle } from 'lucide-react';

interface NewMessageDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onMessageSent: () => void; // Callback to refresh messages
}

// Define PaginatedResponse interface locally or import if defined globally
interface PaginatedResponse<T> {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results: T[];
}

export const NewMessageDialog: React.FC<NewMessageDialogProps> = ({ open, onOpenChange, onMessageSent }) => {
  const { user } = useAuth();
  const [recipients, setRecipients] = useState<UserBasicData[]>([]);
  const [selectedRecipient, setSelectedRecipient] = useState<string>('');
  const [subject, setSubject] = useState<string>('');
  const [content, setContent] = useState<string>('');
  const [isSending, setIsSending] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [usersLoadingError, setUsersLoadingError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setUsersLoadingError(null);
        // Explicitly type the response from accountsAPI.getUsers()
        const response = await accountsAPI.getUsers() as UserBasicData[] | PaginatedResponse<UserBasicData>; 
        const usersArray = Array.isArray(response) ? response : response.results;
        if (!Array.isArray(usersArray)) {
          console.error("Error fetching users: response.results is not an array", response);
          setUsersLoadingError("Failed to load recipients: Invalid data format.");
          return;
        }
        const currentUserId = user?.id ? Number(user.id) : undefined;
        setRecipients(usersArray.filter(u => u.id !== currentUserId));
      } catch (err) {
        console.error("Error fetching users:", err);
        setUsersLoadingError("Failed to load recipients. Please try again.");
      }
    };
    if (open) {
      fetchUsers();
    }
  }, [open, user?.id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedRecipient || !subject.trim() || !content.trim()) {
      setError("Recipient, subject, and message content are required.");
      return;
    }
    setError(null);
    setIsSending(true);

    const messageData: SentMessageData = {
      recipient_id: parseInt(selectedRecipient, 10),
      subject: subject.trim(),
      body: content.trim(),
    };

    try {
      await communicationAPI.createMessage(messageData);
      onMessageSent();
      onOpenChange(false);
      setSelectedRecipient('');
      setSubject('');
      setContent('');
    } catch (err) {
      console.error("Error sending message:", err);
      setError("Failed to send message. Please try again.");
    } finally {
      setIsSending(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>New Message</DialogTitle>
          <DialogDescription>
            Compose and send a new private message.
          </DialogDescription>
        </DialogHeader>
        {usersLoadingError && (
          <Alert variant="destructive" className="mb-4">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{usersLoadingError}</AlertDescription>
          </Alert>
        )}
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="recipient" className="text-right">
                Recipient
              </Label>
              <Select
                value={selectedRecipient}
                onValueChange={setSelectedRecipient}
                disabled={recipients.length === 0 || !!usersLoadingError}
              >
                <SelectTrigger className="col-span-3">
                  <SelectValue placeholder="Select a recipient" />
                </SelectTrigger>
                <SelectContent id="recipient"> {/* It's okay for SelectContent to not have an explicit id prop if not needed by specific styling or logic */}
                  {recipients.map((r) => (
                    <SelectItem key={r.id} value={String(r.id)}>
                      {r.username} ({r.full_name || `${r.first_name || ''} ${r.last_name || ''}`.trim()})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="subject" className="text-right">
                Subject
              </Label>
              <Input
                id="subject"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="col-span-3"
                disabled={!!usersLoadingError}
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="content" className="text-right">
                Message
              </Label>
              <Textarea
                id="content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                className="col-span-3"
                rows={5}
                disabled={!!usersLoadingError}
              />
            </div>
            {error && (
              <Alert variant="destructive" className="col-span-4">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
          </div>
          <DialogFooter>
            <DialogClose asChild>
              <Button type="button" variant="outline">Cancel</Button>
            </DialogClose>
            <Button type="submit" disabled={isSending || !!usersLoadingError}>
              {isSending ? 'Sending...' : 'Send Message'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};
