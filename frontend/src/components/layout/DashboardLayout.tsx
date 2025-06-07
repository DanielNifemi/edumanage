import React, { useState, useCallback } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/useAuth"; // Corrected import path for useAuth hook
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"; // Assuming Sheet components are used for mobile
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Bell,
  BookOpen,
  Calendar,
  ClipboardCheck,
  GraduationCap,
  Home,
  LogOut,
  Menu,
  MessageSquare,
  Settings as SettingsIcon, // Renamed to avoid conflict with Settings page component
  User,
  UserCheck,
  Users,
  BarChart3,
} from "lucide-react";
import { cn } from "@/lib/utils"; // Assuming cn utility is available

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const { user, logout, unreadNotificationsCount, refreshUnreadCount } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const getNavigationItems = useCallback(() => {
    const baseItems = [
      { name: 'Dashboard', href: `/${user?.role}/dashboard`, icon: Home },
      { name: 'Courses', href: '/courses', icon: BookOpen },
      { name: 'Schedule', href: '/schedule', icon: Calendar },
      { name: 'Messages', href: '/messages', icon: MessageSquare },
      { name: 'Announcements', href: '/announcements', icon: MessageSquare },
    ];

    switch (user?.role) {
      case 'student':
        return [
          ...baseItems,
          { name: 'Assignments', href: '/student/assignments', icon: ClipboardCheck },
          { name: 'Attendance', href: '/student/attendance', icon: UserCheck },
        ];
      case 'teacher':
        return [
          ...baseItems,
          { name: 'My Classes', href: '/teacher/classes', icon: Users },
          { name: 'Assignments', href: '/teacher/assignments', icon: ClipboardCheck },
          { name: 'Attendance', href: '/teacher/attendance', icon: UserCheck },
          { name: 'Students', href: '/students', icon: Users },
        ];
      case 'admin':
        return [
          ...baseItems,
          { name: 'Users', href: '/admin/users', icon: Users },
          { name: 'Students', href: '/students', icon: Users },
          { name: 'Teachers', href: '/teachers', icon: Users },
          { name: 'Reports', href: '/admin/reports', icon: BarChart3 },
          { name: 'Site Settings', href: '/admin/settings', icon: SettingsIcon },
        ];
      case 'staff':
        return [
          ...baseItems,
          { name: 'Students', href: '/students', icon: Users },
          { name: 'Teachers', href: '/teachers', icon: Users },
          { name: 'Reports', href: '/staff/reports', icon: BarChart3 },
        ];
      default:
        return baseItems;
    }
  }, [user]);

  const navigationItems = React.useMemo(() => getNavigationItems(), [getNavigationItems]);

  const SidebarContent = () => (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-2 px-6 py-4 border-b">
        <GraduationCap className="h-8 w-8 text-blue-600" />
        <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          EduManage
        </span>
      </div>
      <nav className="flex-1 px-4 py-6 space-y-2">
        {navigationItems.map((item) => {
          const isActive = location.pathname === item.href || (item.href !== '/' && location.pathname.startsWith(item.href));
          return (
            <Link
              key={item.name}
              to={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                isActive
                  ? "bg-blue-100 text-blue-700 dark:bg-blue-700 dark:text-white"
                  : "text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white"
              )}
              onClick={() => setSidebarOpen(false)} // Close mobile sidebar on link click
            >
              <item.icon className="h-5 w-5" />
              {item.name}
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t">
        <div className="flex items-center gap-3">
          <Avatar className="h-10 w-10">
            {/* Use user.profile_data?.profile_image_url */}
            <AvatarImage src={user?.profile_data?.profile_image_url || undefined} /> 
            <AvatarFallback>
              {user?.first_name?.[0]?.toUpperCase()}{user?.last_name?.[0]?.toUpperCase()}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate dark:text-white">
              {user?.first_name} {user?.last_name}
            </p>
            <p className="text-xs text-gray-500 capitalize dark:text-gray-400">{user?.role}</p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex lg:flex-col lg:w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
        <SidebarContent />
      </aside>

      {/* Mobile Sidebar */} 
      <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
        {/* SheetTrigger is handled by the Menu button in the header for mobile */}
        <SheetContent side="left" className="p-0 w-64 bg-white dark:bg-gray-800">
          <SidebarContent />
        </SheetContent>
      </Sheet>

      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 lg:px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                variant="ghost"
                size="icon"
                className="lg:hidden text-gray-600 dark:text-gray-300"
                onClick={() => setSidebarOpen(true)}
              >
                <Menu className="h-6 w-6" />
              </Button>
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white capitalize">
                {/* Dynamically set title based on path or keep it generic */}
                {location.pathname.split('/').pop()?.replace(/-/g, ' ') || 'Dashboard'}
              </h1>
            </div>

            <div className="flex items-center gap-3 sm:gap-4">
              <Link 
                to="/notifications" 
                className="relative text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <Bell className="h-5 w-5" />
                {unreadNotificationsCount > 0 && (
                  <span className="absolute top-0 right-0 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-red-100 bg-red-600 rounded-full transform translate-x-1/2 -translate-y-1/2">
                    {unreadNotificationsCount}
                  </span>
                )}
              </Link>

              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                    <Avatar className="h-10 w-10">
                       {/* Use user.profile_data?.profile_image_url */}
                      <AvatarImage src={user?.profile_data?.profile_image_url || undefined} />
                      <AvatarFallback>
                         {user?.first_name?.[0]?.toUpperCase()}{user?.last_name?.[0]?.toUpperCase()}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56 z-50 bg-white dark:bg-gray-800" align="end" forceMount>
                  <DropdownMenuLabel className="font-normal">
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium leading-none dark:text-white">
                        {user?.first_name} {user?.last_name}
                      </p>
                      <p className="text-xs leading-none text-muted-foreground dark:text-gray-400">
                        {user?.email}
                      </p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator className="dark:bg-gray-700"/>
                  <DropdownMenuItem asChild className="hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer">
                    <Link to="/profile" className="flex items-center gap-2 dark:text-gray-200 w-full">
                      <User className="h-4 w-4" />
                      Profile
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild className="hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer">
                    <Link to="/settings" className="flex items-center gap-2 dark:text-gray-200 w-full">
                      <SettingsIcon className="h-4 w-4" />
                      Settings
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator className="dark:bg-gray-700"/>
                  <DropdownMenuItem onClick={handleLogout} className="hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer flex items-center gap-2 text-red-600 dark:text-red-400 hover:dark:text-red-300 w-full">
                    <LogOut className="h-4 w-4" />
                    Logout
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 dark:bg-gray-950 p-4 sm:p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
