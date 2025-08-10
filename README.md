<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Absence Manager - Face Recognition Attendance System</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            margin-top: 20px;
            margin-bottom: 20px;
        }

        .header {
            text-align: center;
            padding: 40px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            color: white;
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .header h1 {
            font-size: 3.5rem;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }

        .header p {
            font-size: 1.3rem;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }

        .badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 30px 0;
            flex-wrap: wrap;
        }

        .badge {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: bold;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .badge:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }

        .badge.python { background: linear-gradient(45deg, #3776ab, #ffd43b); }
        .badge.pyqt { background: linear-gradient(45deg, #41cd52, #00a651); }
        .badge.mysql { background: linear-gradient(45deg, #00758f, #f29111); }
        .badge.docker { background: linear-gradient(45deg, #0db7ed, #2496ed); }
        .badge.opencv { background: linear-gradient(45deg, #5c85d6, #c41e3a); }

        .section {
            margin: 40px 0;
            padding: 30px;
            border-radius: 15px;
            background: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }

        .section:hover {
            transform: translateY(-5px);
        }

        .section h2 {
            color: #667eea;
            font-size: 2.2rem;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .section h3 {
            color: #764ba2;
            font-size: 1.5rem;
            margin: 25px 0 15px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }

        .feature-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            transition: all 0.3s ease;
        }

        .feature-card:hover {
            transform: translateX(10px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        }

        .feature-card h4 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.2rem;
        }

        .tech-stack {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .tech-item {
            background: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }

        .tech-item:hover {
            transform: scale(1.05);
        }

        .tech-item i {
            font-size: 3rem;
            margin-bottom: 15px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .code-block {
            background: #2d3748;
            color: #e2e8f0;
            padding: 25px;
            border-radius: 12px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            position: relative;
            overflow-x: auto;
        }

        .code-block::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }

        .installation-steps {
            counter-reset: step-counter;
        }

        .step {
            background: #f8f9fa;
            padding: 25px;
            margin: 20px 0;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            position: relative;
            counter-increment: step-counter;
        }

        .step::before {
            content: counter(step-counter);
            position: absolute;
            left: -15px;
            top: 15px;
            background: #667eea;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }

        .step h4 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }

        .project-structure {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            font-family: 'Courier New', monospace;
            line-height: 1.8;
            border: 1px solid #e9ecef;
        }

        .database-schema {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }

        .table-schema {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            border-top: 4px solid #667eea;
        }

        .table-schema h4 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }

        .table-schema ul {
            list-style: none;
            padding: 0;
        }

        .table-schema li {
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
            display: flex;
            justify-content: space-between;
        }

        .table-schema li:last-child {
            border-bottom: none;
        }

        .field-name {
            font-weight: bold;
            color: #764ba2;
        }

        .field-type {
            color: #666;
            font-style: italic;
        }

        .footer {
            text-align: center;
            padding: 40px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px;
            margin-top: 40px;
        }

        .footer h3 {
            margin-bottom: 20px;
            font-size: 1.8rem;
        }

        .social-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        }

        .social-links a {
            color: white;
            font-size: 1.5rem;
            padding: 10px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            text-decoration: none;
        }

        .social-links a:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.1);
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2.5rem;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
            
            .tech-stack {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .badges {
                flex-direction: column;
                align-items: center;
            }
        }

        .highlight {
            background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }

        .warning {
            background: linear-gradient(120deg, #ffecd2 0%, #fcb69f 100%);
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            border-left: 4px solid #ff6b6b;
        }

        .success {
            background: linear-gradient(120deg, #d4ffd4 0%, #a8e6cf 100%);
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            border-left: 4px solid #4CAF50;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1><i class="fas fa-user-graduate"></i> Absence Manager</h1>
            <p>Face Recognition Based Attendance System</p>
            <div class="badges">
                <a href="#" class="badge python"><i class="fab fa-python"></i> Python 3.9</a>
                <a href="#" class="badge pyqt"><i class="fas fa-desktop"></i> PyQt5</a>
                <a href="#" class="badge mysql"><i class="fas fa-database"></i> MySQL</a>
                <a href="#" class="badge docker"><i class="fab fa-docker"></i> Docker</a>
                <a href="#" class="badge opencv"><i class="fas fa-eye"></i> OpenCV</a>
            </div>
        </div>

        <!-- Description -->
        <div class="section">
            <h2><i class="fas fa-info-circle"></i> Project Overview</h2>
            <p style="font-size: 1.1rem; color: #666; line-height: 1.8;">
                This project is a comprehensive Python-based application designed to revolutionize student attendance management using cutting-edge facial recognition technology. It features an intuitive interface developed with PyQt5 and integrates seamlessly with a MySQL database for robust data storage and management.
            </p>
            
            <div class="highlight">
                <h4><i class="fas fa-star"></i> Key Highlight</h4>
                <p>Our system combines artificial intelligence with user-friendly design to create an efficient, accurate, and scalable attendance solution for educational institutions.</p>
            </div>
        </div>

        <!-- Features -->
        <div class="section">
            <h2><i class="fas fa-rocket"></i> Features</h2>
            
            <h3><i class="fas fa-cogs"></i> Core Functionality</h3>
            <div class="features-grid">
                <div class="feature-card">
                    <h4><i class="fas fa-search"></i> Advanced Facial Recognition</h4>
                    <p>Real-time face detection and identification with high accuracy using state-of-the-art algorithms.</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-chart-bar"></i> Comprehensive Analytics</h4>
                    <p>Detailed absence statistics, trends analysis, and interactive reporting capabilities.</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-users"></i> User Management</h4>
                    <p>Complete CRUD operations for student records with photo management and profile editing.</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-envelope"></i> Email Integration</h4>
                    <p>Automated notifications, alerts, and communication with stakeholders.</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-download"></i> Export Capabilities</h4>
                    <p>Export data in multiple formats including PDF, Excel, and text files.</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-shield-alt"></i> Security Features</h4>
                    <p>Protected access with authentication codes and secure data handling.</p>
                </div>
            </div>

            <h3><i class="fas fa-paint-brush"></i> User Interface</h3>
            <ul style="margin-left: 20px; line-height: 2;">
                <li><strong>Modern PyQt5 Interface</strong> - Responsive and intuitive design</li>
                <li><strong>Multi-language Support</strong> - French/English interface options</li>
                <li><strong>Real-time Updates</strong> - Live data synchronization and instant feedback</li>
                <li><strong>Interactive Charts</strong> - Dynamic visualization of attendance data</li>
            </ul>
        </div>

        <!-- Technology Stack -->
        <div class="section">
            <h2><i class="fas fa-layer-group"></i> Technology Stack</h2>
            <div class="tech-stack">
                <div class="tech-item">
                    <i class="fab fa-python"></i>
                    <h4>Python 3.9</h4>
                    <p>Backend Logic</p>
                </div>
                <div class="tech-item">
                    <i class="fas fa-desktop"></i>
                    <h4>PyQt5</h4>
                    <p>User Interface</p>
                </div>
                <div class="tech-item">
                    <i class="fas fa-database"></i>
                    <h4>MySQL</h4>
                    <p>Data Storage</p>
                </div>
                <div class="tech-item">
                    <i class="fab fa-docker"></i>
                    <h4>Docker</h4>
                    <p>Containerization</p>
                </div>
                <div class="tech-item">
                    <i class="fas fa-eye"></i>
                    <h4>OpenCV</h4>
                    <p>Computer Vision</p>
                </div>
                <div class="tech-item">
                    <i class="fas fa-brain"></i>
                    <h4>Face Recognition</h4>
                    <p>AI Processing</p>
                </div>
            </div>
        </div>

        <!-- Project Structure -->
        <div class="section">
            <h2><i class="fas fa-folder-tree"></i> Project Structure</h2>
            <div class="project-structure">
FACE-RECOGNITION-APP/
│
├── 📁 python/
│   ├── 🐍 Menu.py                        # Main application entry point
│   ├── 🎯 recorder.py                    # Face recognition recording module
│   ├── 📊 AbsenceAnalyticsInterface.py   # Analytics and statistics interface
│   ├── 🏠 AbsenceManagerHome.py          # Home dashboard interface
│   ├── 👥 ManageUsersInterface.py        # User management interface
│   ├── 📧 NotifiInterface.py             # Notification system
│   ├── 📋 requirements.txt               # Python dependencies
│   └── 🐳 Dockerfile                     # Python app containerization
│
├── 📁 mysql/
│   ├── 🗄️ database_students.sql          # Database initialization script
│   └── 🐳 Dockerfile                     # MySQL containerization
│
├── 🐳 docker-compose.yml                 # Multi-container orchestration
└── 📖 README.md                          # Project documentation
            </div>
        </div>

        <!-- Database Schema -->
        <div class="section">
            <h2><i class="fas fa-database"></i> Database Schema</h2>
            <div class="database-schema">
                <div class="table-schema">
                    <h4><i class="fas fa-table"></i> Users Table</h4>
                    <ul>
                        <li><span class="field-name">id</span> <span class="field-type">INT AUTO_INCREMENT PRIMARY KEY</span></li>
                        <li><span class="field-name">username</span> <span class="field-type">VARCHAR(255) UNIQUE</span></li>
                        <li><span class="field-name">filiere</span> <span class="field-type">VARCHAR(255)</span></li>
                        <li><span class="field-name">image</span> <span class="field-type">LONGBLOB</span></li>
                        <li><span class="field-name">image_pure</span> <span class="field-type">LONGBLOB</span></li>
                        <li><span class="field-name">accepte</span> <span class="field-type">INT</span></li>
                    </ul>
                </div>
                <div class="table-schema">
                    <h4><i class="fas fa-table"></i> Absence Table</h4>
                    <ul>
                        <li><span class="field-name">id_ab</span> <span class="field-type">INT AUTO_INCREMENT PRIMARY KEY</span></li>
                        <li><span class="field-name">id</span> <span class="field-type">INT FOREIGN KEY</span></li>
                        <li><span class="field-name">time</span> <span class="field-type">VARCHAR(255)</span></li>
                        <li><span class="field-name">date</span> <span class="field-type">VARCHAR(255)</span></li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Installation Guide -->
        <div class="section">
            <h2><i class="fas fa-download"></i> Installation Guide</h2>
            
            <div class="warning">
                <h4><i class="fas fa-exclamation-triangle"></i> Prerequisites</h4>
                <p>Ensure you have Docker and Docker Compose installed on your system before proceeding.</p>
            </div>

            <div class="installation-steps">
                <div class="step">
                    <h4><i class="fas fa-download"></i> Install Docker</h4>
                    <p>Download and install Docker from the <a href="https://docs.docker.com/get-docker/" target="_blank">official Docker website</a>.</p>
                </div>

                <div class="step">
                    <h4><i class="fas fa-puzzle-piece"></i> Install Docker Compose</h4>
                    <p>Download and install Docker Compose from the <a href="https://docs.docker.com/compose/install/" target="_blank">official Docker Compose page</a>.</p>
                </div>

                <div class="step">
                    <h4><i class="fas fa-desktop"></i> Setup XLauncher (Windows)</h4>
                    <p>Install XLauncher for GUI support:</p>
                    <ul style="margin-left: 20px; margin-top: 10px;">
                        <li>Choose "Multiple windows" display, number 0</li>
                        <li>Select "Start with no client"</li>
                        <li>Activate "Disable Access Control"</li>
                    </ul>
                </div>

                <div class="step">
                    <h4><i class="fas fa-network-wired"></i> Create Docker Network</h4>
                    <div class="code-block">
docker network create testg_network
                    </div>
                </div>

                <div class="step">
                    <h4><i class="fas fa-cloud-download-alt"></i> Pull Docker Images</h4>
                    <div class="code-block">
docker pull jammiosama/face-recognition-app-mysql:latest
docker pull jammiosama/face-recognition-app-pythonapp:latest
                    </div>
                </div>

                <div class="step">
                    <h4><i class="fas fa-database"></i> Start MySQL Container</h4>
                    <div class="code-block">
docker run --name face-recognition-app-mysql-1 \
    --network testg_network \
    -e MYSQL_ROOT_PASSWORD=root \
    -d jammiosama/face-recognition-app-mysql:latest
                    </div>
                </div>

                <div class="step">
                    <h4><i class="fas fa-play"></i> Launch Application</h4>
                    <p>Replace <code>192.168.0.71</code> with your actual IP address:</p>
                    <div class="code-block">
docker run --rm --name test-pythonapp \
    --network testg_network \
    -e DISPLAY=192.168.0.71:0 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    jammiosama/face-recognition-app-pythonapp:latest
                    </div>
                </div>
            </div>

            <div class="success">
                <h4><i class="fas fa-check-circle"></i> Installation Complete!</h4>
                <p>Your Absence Manager system is now ready to use. The application will automatically create the necessary database tables on first run.</p>
            </div>
        </div>

        <!-- Usage -->
        <div class="section">
            <h2><i class="fas fa-play-circle"></i> Usage</h2>
            
            <h3><i class="fas fa-home"></i> Main Dashboard</h3>
            <ul style="margin-left: 20px; line-height: 2;">
                <li><strong>Record Absence:</strong> Launch the facial recognition system</li>
                <li><strong>Manage Users:</strong> Add, edit, or remove student records</li>
                <li><strong>Absence Analysis:</strong> View detailed statistics and reports</li>
                <li><strong>Notifications:</strong> Check email notifications and alerts</li>
            </ul>

            <h3><i class="fas fa-camera"></i> Face Recognition Process</h3>
            <div class="features-grid">
                <div class="feature-card">
                    <h4>1. Camera Initialization</h4>
                    <p>System activates the camera and loads known face encodings from the database.</p>
                </div>
                <div class="feature-card">
                    <h4>2. Real-time Detection</h4>
                    <p>Continuous face detection and recognition with confidence scoring.</p>
                </div>
                <div class="feature-card">
                    <h4>3. Attendance Marking</h4>
                    <p>Automatic attendance recording for recognized students with timestamp.</p>
                </div>
                <div class="feature-card">
                    <h4>4. Session Completion</h4>
                    <p>Secure session termination with code verification and batch absence recording.</p>
                </div>
            </div>
        </div>

        <!-- Contributing -->
        <div class="section">
            <h2><i class="fas fa-hands-helping"></i> Contributing</h2>
            <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 20px;">
                We welcome contributions to improve the Absence Manager system! Here's how you can contribute:
            </p>
            
            <div class="features-grid">
                <div class="feature-card">
                    <h4><i class="fas fa-code-branch"></i> Fork the Repository</h4>
                    <p>Create your own fork of the project to work on improvements.</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-bug"></i> Report Issues</h4>
                    <p>Submit bug reports or feature requests through the issue tracker.</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-pull-request"></i> Submit Pull Requests</h4>
                    <p>Propose changes and improvements through pull requests.</p>
                </div>
                <div class="feature-card">
                    <h4><i class="fas fa-book"></i> Improve Documentation</h4>
                    <p>Help enhance the documentation and user guides.</p>
                </div>
            </div>

            <div class="highlight">
                <h4><i class="fas fa-lightbulb"></i> Development Guidelines</h4>
                <ul style="margin-left: 20px; line-height: 1.8;">
                    <li>Follow PEP 8 coding standards for Python code</li>
                    <li>Add comprehensive comments and docstrings</li>
                    <li>Test your changes thoroughly before submitting</li>
                    <li>Update documentation for any new features</li>
                </ul>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <h3><i class="fas fa-heart"></i> Made with Passion</h3>
            <p>Developed for educational institutions to streamline attendance management</p>
            <div class="social-links">
                <a href="#"><i class="fab fa-github"></i></a>
                <a href="#"><i class="fab fa-linkedin"></i></a>
                <a href="#"><i class="fab fa-twitter"></i></a>
                <a href="#"><i class="fas fa-envelope"></i></a>
            </div>
            <p style="margin-top: 20px; opacity: 0.8;">
                © 2024 Absence Manager. Licensed under MIT License.
            </p>
        </div>
    </div>

    <script>
        // Add smooth scrolling for any anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Add scroll-triggered animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.section').forEach(section => {
            section.style.opacity = '0';
            section.style.transform = 'translateY(30px)';
            section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(section);
        });

        // Add interactive hover effects for feature cards
        document.querySelectorAll('.feature-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    </script>
</body>
</html>
