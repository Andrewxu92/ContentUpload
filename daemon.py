#!/usr/bin/env python3.4

import os,sys,time,atexit,signal,socket

class CDaemon:
	def __init__(self,pidfile,stdin='/dev/null',stdout='/dev/null',stderr='/dev/null'):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile
	
	def daemonize(self):
		if os.path.exists(self.pidfile):
			raise RuntimeError('Already running')

		try: 
			if os.fork()>0:
				raise SystemExit(0)
		except OSError as e :
			raise RuntimeError('fork #1 failed')

		os.chdir('/')
		os.umask(0)
		os.setsid()
		
		try:
			if os.fork()>0:
				raise SystemExit(0)
		except OSError as e:
			raise RuntimeError('fork #2 failed')

		sys.stdout.flush()
		sys.stderr.flush()

		with open(self.stdin,'rb',0) as f:
			os.dup2(f.fileno(), sys.stdin.fileno())
		with open(self.stdout,'ab',0) as f:
			os.dup2(f.fileno(), sys.stdout.fileno())
		with open(self.stderr,'ab',0) as f:
			os.dup2(f.fileno(), sys.stderr.fileno())

		with open(self.pidfile,'w') as f:
			print (os.getpid(), file=f)

		atexit.register(lambda: os.remove(self.pidfile))

		def sigterm_handler(signo, frame):
			raise SystemExit(1)

		signal.signal(signal.SIGTERM, sigterm_handler)

	def run(self):
		while True:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.bind(('172.31.0.126', 9000))
			sock.listen(5)
			print("server is listening port 9000")
			while True:
				connection, address = sock.accept()
				try:
					connection.settimeout(50)
					while True:
						buf = connection.recv(1024)	
						if (buf):
							print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
							print(buf.decode())
						else:
							break
				except socket.timeout:
					print ("time out")
				except (ConnectionResetError):
					pass
					time.sleep(0.01)
				except (UnicodeDecodeError):
					pass
				except Exception as e:
					print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
					print (e)
					raise SystemExit(1)
			connection.close()
			print ("closing")


	def start(self):
		try:
			self.daemonize()
			print ('Start run\n')
			self.run()
		except RuntimeError as e:
			print ('Cant Start Daemon\n')
			print (e, file=sys.stderr)
			raise SystemExit(1)
	
	def stop(self):
		if os.path.exists(self.pidfile):
			with open(self.pidfile) as f:
				os.kill(int(f.read()),signal.SIGTERM)
		else:
			print ('Not Running\n')
			raise SystemExit(1)

	def status(self):
		return 0



if __name__ == '__main__':
	PIDFILE = '/tmp/daemon.pid'
	cd = CDaemon(pidfile=PIDFILE,stdout = '/home/ubuntu/AWSHCA/port.log',stderr='/home/ubuntu/AWSHCA/err.log')
	if len(sys.argv) != 2:
		print ('Usage : {}. [start|stop]'.format(sys.argv[0], file=sys.stderr))
		raise SystemExit(1)
		
	if sys.argv[1] == 'start':
		try:
			cd.start()
		except RuntimeError as e :
			print (e, file=sys.stderr)
			raise SystemExit(1)
		
	elif sys.argv[1] == 'stop':
		cd.stop()

	else:
		print ('Unknown Command')
		raise SystemExit(1)
			
				
