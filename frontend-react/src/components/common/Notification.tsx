import React, { useEffect } from 'react';
import type { Notification as NotificationType } from '../../types';

interface NotificationProps {
  notification: NotificationType;
  onClose: (id: string) => void;
}

const Notification: React.FC<NotificationProps> = ({ notification, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose(notification.id);
    }, 5000);

    return () => clearTimeout(timer);
  }, [notification.id, onClose]);

  const bgColor = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    info: 'bg-blue-500',
    warning: 'bg-yellow-500',
  }[notification.type];

  return (
    <div
      className={`${bgColor} text-white px-6 py-4 rounded-lg shadow-lg flex items-center justify-between max-w-md animate-slide-in`}
    >
      <span>{notification.message}</span>
      <button
        onClick={() => onClose(notification.id)}
        className="ml-4 text-white hover:text-gray-200 text-xl font-bold"
      >
        ×
      </button>
    </div>
  );
};

export default Notification;
