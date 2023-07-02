import subprocess

if __name__ == '__main__':

    app1_process = subprocess.Popen(['python3', 'login.py'])
    app2_process = subprocess.Popen(['python3', 'system-monitor.py'])
    app3_process = subprocess.Popen(['python3', 'analytics.py'])
    app4_process = subprocess.Popen(['python3', 'reports.py'])
    app5_process = subprocess.Popen(['python3', 'security.py'])
    app6_process = subprocess.Popen(['python3', 'settings.py'])

    app1_process.wait()
    app2_process.wait()
    app3_process.wait()
    app4_process.wait()
    app5_process.wait()
    app6_process.wait()
