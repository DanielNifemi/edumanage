
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Search, Plus, Send, Paperclip } from "lucide-react";
import { useState } from "react";

const Messages = () => {
  const [selectedMessage, setSelectedMessage] = useState<number | null>(1);
  const [newMessage, setNewMessage] = useState("");

  const conversations = [
    {
      id: 1,
      sender: "Dr. Smith",
      subject: "Assignment Feedback",
      preview: "Great work on your latest submission...",
      time: "2 hours ago",
      unread: true,
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face"
    },
    {
      id: 2,
      sender: "Prof. Johnson",
      subject: "Math Exam Schedule",
      preview: "The midterm exam has been rescheduled...",
      time: "5 hours ago",
      unread: false,
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face"
    },
    {
      id: 3,
      sender: "Jane Smith",
      subject: "Study Group",
      preview: "Are you interested in joining our study group...",
      time: "1 day ago",
      unread: true,
      avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face"
    },
    {
      id: 4,
      sender: "Academic Office",
      subject: "Registration Reminder",
      preview: "Don't forget to register for next semester...",
      time: "2 days ago",
      unread: false,
      avatar: "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=150&h=150&fit=crop&crop=face"
    },
  ];

  const currentConversation = conversations.find(c => c.id === selectedMessage);

  const messageThread = [
    {
      id: 1,
      sender: "Dr. Smith",
      content: "Hi there! I wanted to give you feedback on your latest assignment submission. Overall, you did an excellent job demonstrating understanding of the core concepts.",
      time: "2:30 PM",
      isMe: false
    },
    {
      id: 2,
      sender: "You",
      content: "Thank you for the feedback! I'm glad the concepts came through clearly. Are there any specific areas you think I should focus on for improvement?",
      time: "2:45 PM",
      isMe: true
    },
    {
      id: 3,
      sender: "Dr. Smith",
      content: "I'd suggest working on the implementation details in section 3. Your logic is sound, but the code could be more efficient. Would you like to discuss this during office hours?",
      time: "3:15 PM",
      isMe: false
    }
  ];

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      // Handle sending message
      setNewMessage("");
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Messages</h1>
            <p className="text-gray-600">Communicate with teachers and classmates</p>
          </div>
          <Button className="flex items-center gap-2">
            <Plus className="h-4 w-4" />
            New Message
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-200px)]">
          {/* Messages List */}
          <Card className="border-0 shadow-md lg:col-span-1">
            <CardHeader>
              <CardTitle>Conversations</CardTitle>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input placeholder="Search messages..." className="pl-10" />
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="space-y-1">
                {conversations.map((conversation) => (
                  <div
                    key={conversation.id}
                    className={`p-4 cursor-pointer border-b hover:bg-gray-50 ${
                      selectedMessage === conversation.id ? 'bg-blue-50 border-l-4 border-l-blue-500' : ''
                    }`}
                    onClick={() => setSelectedMessage(conversation.id)}
                  >
                    <div className="flex items-start gap-3">
                      <Avatar className="h-10 w-10">
                        <AvatarImage src={conversation.avatar} />
                        <AvatarFallback>{conversation.sender[0]}</AvatarFallback>
                      </Avatar>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <h4 className="font-medium text-sm truncate">{conversation.sender}</h4>
                          <span className="text-xs text-gray-500">{conversation.time}</span>
                        </div>
                        <p className="font-medium text-sm mb-1 truncate">{conversation.subject}</p>
                        <p className="text-xs text-gray-600 truncate">{conversation.preview}</p>
                        {conversation.unread && (
                          <Badge variant="default" className="mt-1">New</Badge>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Message Thread */}
          <Card className="border-0 shadow-md lg:col-span-2 flex flex-col">
            {currentConversation ? (
              <>
                <CardHeader className="border-b">
                  <div className="flex items-center gap-3">
                    <Avatar className="h-10 w-10">
                      <AvatarImage src={currentConversation.avatar} />
                      <AvatarFallback>{currentConversation.sender[0]}</AvatarFallback>
                    </Avatar>
                    <div>
                      <CardTitle className="text-lg">{currentConversation.sender}</CardTitle>
                      <CardDescription>{currentConversation.subject}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent className="flex-1 p-6 overflow-y-auto">
                  <div className="space-y-4">
                    {messageThread.map((message) => (
                      <div key={message.id} className={`flex ${message.isMe ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                          message.isMe 
                            ? 'bg-blue-500 text-white' 
                            : 'bg-gray-100 text-gray-900'
                        }`}>
                          <p className="text-sm">{message.content}</p>
                          <p className={`text-xs mt-1 ${
                            message.isMe ? 'text-blue-100' : 'text-gray-500'
                          }`}>
                            {message.time}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>

                <div className="border-t p-4">
                  <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm">
                      <Paperclip className="h-4 w-4" />
                    </Button>
                    <Input
                      placeholder="Type your message..."
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                      className="flex-1"
                    />
                    <Button onClick={handleSendMessage}>
                      <Send className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </>
            ) : (
              <CardContent className="flex-1 flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <p>Select a conversation to start messaging</p>
                </div>
              </CardContent>
            )}
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Messages;
