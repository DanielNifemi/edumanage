
import DashboardLayout from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Calendar, Clock, MapPin, ChevronLeft, ChevronRight } from "lucide-react";
import { useState } from "react";

const Schedule = () => {
  const [currentWeek, setCurrentWeek] = useState(new Date());

  const schedule = {
    Monday: [
      { id: 1, subject: "Computer Science", time: "09:00 - 10:30", room: "Lab 101", instructor: "Dr. Smith" },
      { id: 2, subject: "Mathematics", time: "11:00 - 12:30", room: "Room 205", instructor: "Prof. Johnson" },
      { id: 3, subject: "Physics", time: "14:00 - 15:30", room: "Lab 301", instructor: "Dr. Wilson" },
    ],
    Tuesday: [
      { id: 4, subject: "English Literature", time: "10:00 - 11:30", room: "Room 102", instructor: "Ms. Brown" },
      { id: 5, subject: "Chemistry", time: "13:00 - 14:30", room: "Lab 201", instructor: "Dr. Davis" },
    ],
    Wednesday: [
      { id: 6, subject: "Computer Science", time: "09:00 - 10:30", room: "Lab 101", instructor: "Dr. Smith" },
      { id: 7, subject: "History", time: "11:00 - 12:30", room: "Room 103", instructor: "Mr. Taylor" },
    ],
    Thursday: [
      { id: 8, subject: "Mathematics", time: "09:00 - 10:30", room: "Room 205", instructor: "Prof. Johnson" },
      { id: 9, subject: "Biology", time: "14:00 - 15:30", room: "Lab 302", instructor: "Dr. Anderson" },
    ],
    Friday: [
      { id: 10, subject: "Physics", time: "10:00 - 11:30", room: "Lab 301", instructor: "Dr. Wilson" },
      { id: 11, subject: "Chemistry", time: "13:00 - 14:30", room: "Lab 201", instructor: "Dr. Davis" },
    ],
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('en-US', { 
      month: 'long', 
      day: 'numeric', 
      year: 'numeric' 
    });
  };

  const getWeekDates = (startDate: Date) => {
    const week = [];
    const start = new Date(startDate);
    start.setDate(start.getDate() - start.getDay() + 1); // Start from Monday
    
    for (let i = 0; i < 5; i++) {
      const date = new Date(start);
      date.setDate(start.getDate() + i);
      week.push(date);
    }
    return week;
  };

  const weekDates = getWeekDates(currentWeek);
  const weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

  const navigateWeek = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentWeek);
    newDate.setDate(newDate.getDate() + (direction === 'next' ? 7 : -7));
    setCurrentWeek(newDate);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Schedule</h1>
            <p className="text-gray-600">Your weekly class schedule</p>
          </div>
          <Button className="flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            View Calendar
          </Button>
        </div>

        {/* Week Navigation */}
        <Card className="border-0 shadow-md">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigateWeek('prev')}
              >
                <ChevronLeft className="h-4 w-4" />
                Previous Week
              </Button>
              
              <h2 className="text-xl font-semibold">
                Week of {formatDate(weekDates[0])}
              </h2>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigateWeek('next')}
              >
                Next Week
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Schedule Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          {weekDays.map((day, index) => (
            <Card key={day} className="border-0 shadow-md">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg">{day}</CardTitle>
                <CardDescription>
                  {weekDates[index]?.toLocaleDateString('en-US', { 
                    month: 'short', 
                    day: 'numeric' 
                  })}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {schedule[day as keyof typeof schedule]?.map((class_item) => (
                    <div key={class_item.id} className="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                      <h4 className="font-medium text-sm text-gray-900 mb-1">
                        {class_item.subject}
                      </h4>
                      <div className="space-y-1">
                        <div className="flex items-center gap-1 text-xs text-gray-600">
                          <Clock className="h-3 w-3" />
                          {class_item.time}
                        </div>
                        <div className="flex items-center gap-1 text-xs text-gray-600">
                          <MapPin className="h-3 w-3" />
                          {class_item.room}
                        </div>
                        <p className="text-xs text-gray-500">{class_item.instructor}</p>
                      </div>
                    </div>
                  )) || (
                    <p className="text-sm text-gray-500 text-center py-4">No classes</p>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Today's Summary */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle>Today's Classes</CardTitle>
            <CardDescription>Your schedule for today</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {schedule.Monday.map((class_item) => (
                <div key={class_item.id} className="p-4 border rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-medium">{class_item.subject}</h4>
                    <Badge variant="outline">Upcoming</Badge>
                  </div>
                  <div className="space-y-1 text-sm text-gray-600">
                    <div className="flex items-center gap-2">
                      <Clock className="h-4 w-4" />
                      {class_item.time}
                    </div>
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4" />
                      {class_item.room}
                    </div>
                    <p>{class_item.instructor}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default Schedule;
