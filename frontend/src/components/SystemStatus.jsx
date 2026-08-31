import { useState, useEffect } from 'react';
import axios from 'axios';

export default function SystemStatus() {
  const [status, setStatus] = useState('checking...');

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const resp = await axios.get('http://localhost:8000/system/status');
        setStatus(resp.data.status);
      } catch (e) {
        setStatus('offline');
      }
    };
    checkStatus();
  }, []);

  return (
    <div className="border p-4 rounded mt-4">
      <h3 className="font-bold">System Status</h3>
      <p>API: <span className={status === 'online' ? 'text-green-500' : 'text-red-500'}>{status}</span></p>
    </div>
  );
}
