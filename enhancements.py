<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IELTS Smart Study Plan Generator</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }

        /* Enhanced Header - Clean & Focused */
        .app-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
            position: relative;
            overflow: hidden;
        }

        .app-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="1" fill="%23ffffff" opacity="0.05"/><circle cx="80" cy="80" r="1" fill="%23ffffff" opacity="0.05"/><circle cx="40" cy="60" r="1" fill="%23ffffff" opacity="0.05"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            pointer-events: none;
        }

        .header-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
            position: relative;
            z-index: 2;
        }

        .brand-section {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .logo {
            width: 80px;
            height: 80px;
            background: white;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease;
        }

        .logo:hover {
            transform: scale(1.05) rotate(5deg);
        }

        .logo img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 8px;
        }

        .brand-text h1 {
            font-size: 2.8rem;
            margin: 0;
            font-weight: 800;
            background: linear-gradient(45deg, #ffffff, #e6f3ff, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            letter-spacing: -1px;
            position: relative;
        }

        .brand-text h1::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, #ffffff, transparent);
            border-radius: 2px;
        }

        .brand-text .tagline {
            margin: 0.5rem 0 0 0;
            opacity: 0.95;
            font-size: 1rem;
            font-weight: 300;
            color: #e6f3ff;
            font-style: italic;
            letter-spacing: 0.5px;
        }

        .language-selector select {
            padding: 0.75rem 1.25rem;
            border-radius: 12px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.15);
            color: white;
            font-weight: 500;
            cursor: pointer;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            font-size: 1rem;
        }

        .language-selector select:hover {
            background: rgba(255, 255, 255, 0.25);
            border-color: rgba(255, 255, 255, 0.5);
        }

        .language-selector select option {
            color: #333;
            background: white;
        }

        /* Main Generator Form - Enhanced */
        .main-content {
            max-width: 900px;
            margin: 3rem auto;
            padding: 0 2rem;
        }

        .generator-form {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            position: relative;
            overflow: hidden;
        }

        .generator-form::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
            background-size: 200% 100%;
            animation: shimmer 3s ease-in-out infinite;
        }

        @keyframes shimmer {
            0%, 100% { background-position: 200% 0; }
            50% { background-position: -200% 0; }
        }

        .form-title {
            font-size: 2.2rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 2.5rem;
            font-weight: 700;
            position: relative;
        }

        .form-title::after {
            content: '✨';
            position: absolute;
            top: -10px;
            right: -20px;
            font-size: 1.5rem;
            animation: sparkle 2s ease-in-out infinite;
        }

        @keyframes sparkle {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.2); }
        }

        .form-group {
            margin-bottom: 2rem;
        }

        .form-label {
            display: block;
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 0.75rem;
            font-size: 1.1rem;
        }

        .form-select {
            width: 100%;
            padding: 1rem 1.25rem;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1.1rem;
            background: white;
            color: #2d3748;
            transition: all 0.3s ease;
            font-family: 'Poppins', sans-serif;
        }

        .form-select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
            transform: translateY(-2px);
        }

        .generate-btn {
            width: 100%;
            padding: 1.25rem 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 16px;
            font-size: 1.25rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.4s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }

        .generate-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s ease;
        }

        .generate-btn:hover::before {
            left: 100%;
        }

        .generate-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        }

        /* Resources Section - Moved to Bottom with Color Coding */
        .resources-section {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 4rem 0;
            margin-top: 4rem;
        }

        .resources-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        .resources-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 3rem;
            position: relative;
        }

        .resources-title::before {
            content: '🌟';
            display: block;
            font-size: 3rem;
            margin-bottom: 1rem;
            animation: bounce 2s ease-in-out infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .resources-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }

        /* Color-coded skill categories */
        .skill-listening {
            background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
            border-left: 5px solid #ff4757;
        }

        .skill-reading {
            background: linear-gradient(135deg, #4ecdc4, #6bcf7f);
            border-left: 5px solid #2ed573;
        }

        .skill-writing {
            background: linear-gradient(135deg, #45b7d1, #4834d4);
            border-left: 5px solid #3742fa;
        }

        .skill-speaking {
            background: linear-gradient(135deg, #f39c12, #f1c40f);
            border-left: 5px solid #e67e22;
        }

        .skill-vocabulary {
            background: linear-gradient(135deg, #9b59b6, #8e44ad);
            border-left: 5px solid #7d3c98;
        }

        .skill-resources {
            background: linear-gradient(135deg, #16a085, #27ae60);
            border-left: 5px solid #148f77;
        }

        .skill-blog {
            background: linear-gradient(135deg, #e67e22, #d35400);
            border-left: 5px solid #c0392b;
        }

        .skill-official {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            border-left: 5px solid #1a252f;
        }

        .resource-category {
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            color: white;
        }

        .resource-category::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            transform: translate(30px, -30px);
        }

        .resource-category:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }

        .category-title {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-weight: 700;
            font-size: 1.3rem;
            margin-bottom: 1.5rem;
            position: relative;
            z-index: 2;
        }

        .category-title i {
            font-size: 1.5rem;
            padding: 0.5rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 12px;
        }

        .resource-links {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            position: relative;
            z-index: 2;
        }

        .resource-link {
            color: rgba(255, 255, 255, 0.95);
            text-decoration: none;
            padding: 0.75rem 1rem;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.15);
            transition: all 0.3s ease;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-weight: 500;
            backdrop-filter: blur(10px);
        }

        .resource-link:hover {
            background: rgba(255, 255, 255, 0.25);
            color: white;
            transform: translateX(8px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .resource-link i {
            font-size: 0.9rem;
            opacity: 0.9;
            min-width: 16px;
        }

        .external-link {
            border-left: 3px solid rgba(255, 255, 255, 0.4);
            padding-left: 1.5rem;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .header-container {
                flex-direction: column;
                gap: 1.5rem;
                text-align: center;
            }

            .brand-text h1 {
                font-size: 2rem;
            }

            .logo {
                width: 60px;
                height: 60px;
            }

            .resources-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }

            .resource-category {
                padding: 1.5rem;
            }

            .resources-container, .header-container, .main-content {
                padding: 0 1rem;
            }

            .generator-form {
                padding: 2rem;
            }

            .form-title {
                font-size: 1.8rem;
            }
        }

        @media (max-width: 480px) {
            .brand-section {
                flex-direction: column;
                gap: 1rem;
            }

            .brand-text h1 {
                font-size: 1.6rem;
            }

            .logo {
                width: 50px;
                height: 50px;
            }

            .resource-links {
                gap: 0.5rem;
            }

            .resource-link {
                padding: 0.6rem 0.8rem;
                font-size: 0.9rem;
            }

            .resources-title {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <!-- Clean Header - Focused on Generator -->
    <header class="app-header">
        <div class="header-container">
            <div class="brand-section">
                <div class="logo">
                    <img src="/static/images/your-logo-name.png" alt="SparkSkyTech Logo">
                    <!-- Fallback with your logo colors -->
                    <div style="width:100%; height:100%; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%); border-radius: 16px; display: flex; align-items: center; justify-content: center; position: relative;">
                        <div style="color: white; font-weight: bold; font-size: 24px;">SST</div>
                        <div style="position: absolute; top: 5px; right: 8px; width: 20px; height: 20px; background: rgba(255,255,255,0.3); border-radius: 50%; transform: rotate(45deg);"></div>
                        <div style="position: absolute; bottom: 8px; left: 6px; width: 15px; height: 15px; background: rgba(255,255,255,0.2); border-radius: 50%;"></div>
                    </div>
                </div>
                <div class="brand-text">
                    <h1>IELTS Smart Study Plan Generator</h1>
                    <p class="tagline">✨ Personalized Learning, Proven Results ✨</p>
                </div>
            </div>
            <div class="language-selector">
                <select name="language" id="language">
                    <option value="en">🇺🇸 English</option>
                    <option value="ar">🇸🇦 العربية</option>
                </select>
            </div>
        </div>
    </header>

    <!-- Main Generator Form -->
    <main class="main-content">
        <div class="generator-form">
            <h2 class="form-title">Generate Your Personalized Study Plan</h2>
            
            <form id="studyPlanForm">
                <div class="form-group">
                    <label for="currentLevel" class="form-label">Your current English level:</label>
                    <select id="currentLevel" name="currentLevel" class="form-select" required>
                        <option value="">-- Select your level --</option>
                        <option value="beginner">Beginner (A1-A2)</option>
                        <option value="intermediate">Intermediate (B1-B2)</option>
                        <option value="advanced">Advanced (C1-C2)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="targetBand" class="form-label">Target IELTS Band:</label>
                    <select id="targetBand" name="targetBand" class="form-select" required>
                        <option value="">-- Select target band --</option>
                        <option value="5.5">Band 5.5</option>
                        <option value="6.0">Band 6.0</option>
                        <option value="6.5">Band 6.5</option>
                        <option value="7.0">Band 7.0</option>
                        <option value="7.5">Band 7.5</option>
                        <option value="8.0">Band 8.0</option>
                        <option value="8.5">Band 8.5</option>
                        <option value="9.0">Band 9.0</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="testType" class="form-label">Test Type:</label>
                    <select id="testType" name="testType" class="form-select" required>
                        <option value="">-- Select test type --</option>
                        <option value="academic">Academic IELTS</option>
                        <option value="general">General Training IELTS</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="testMode" class="form-label">Test Mode:</label>
                    <select id="testMode" name="testMode" class="form-select" required>
                        <option value="">-- Select test mode --</option>
                        <option value="paper">Paper-based</option>
                        <option value="computer">Computer-based</option>
                        <option value="online">Online IELTS</option>
                    </select>
                </div>

                <button type="submit" class="generate-btn">
                    <i class="fas fa-magic"></i> Generate My Study Plan
                </button>
            </form>
        </div>
    </main>

    <!-- Resources Section - Moved to Bottom with Color Coding -->
    <section class="resources-section">
        <div class="resources-container">
            <h2 class="resources-title">Comprehensive IELTS Resources by SparkSkyTech</h2>
            <div class="resources-grid">
                <!-- Listening Skills - Red Theme -->
                <div class="resource-category skill-listening">
                    <div class="category-title">
                        <i class="fas fa-headphones"></i>
                        Listening Skills
                    </div>
                    <div class="resource-links">
                        <a href="https://www.sparkskytech.com/ielts/ielts-listening" class="resource-link" target="_blank">
                            <i class="fas fa-play-circle"></i>
                            IELTS Listening Preparation
                        </a>
                        <a href="https://www.ielts.org/for-test-takers/test-format/listening" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            Official IELTS Listening Format
                        </a>
                        <a href="https://takeielts.britishcouncil.org/take-ielts/prepare/practice-tests" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            British Council Practice Tests
                        </a>
                    </div>
                </div>

                <!-- Reading Skills - Green Theme -->
                <div class="resource-category skill-reading">
                    <div class="category-title">
                        <i class="fas fa-book-open"></i>
                        Reading Skills
                    </div>
                    <div class="resource-links">
                        <a href="https://www.sparkskytech.com/ielts/ielts-reading" class="resource-link" target="_blank">
                            <i class="fas fa-bookmark"></i>
                            IELTS Reading Strategies
                        </a>
                        <a href="https://www.ielts.org/for-test-takers/test-format/reading" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            Official Reading Format
                        </a>
                        <a href="https://ieltsliz.com/ielts-reading-tips/" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            IELTS Liz Reading Tips
                        </a>
                    </div>
                </div>

                <!-- Writing Skills - Blue Theme -->
                <div class="resource-category skill-writing">
                    <div class="category-title">
                        <i class="fas fa-pen-fancy"></i>
                        Writing Skills
                    </div>
                    <div class="resource-links">
                        <a href="https://www.sparkskytech.com/ielts/ielts-writing-preparation" class="resource-link" target="_blank">
                            <i class="fas fa-edit"></i>
                            IELTS Writing Preparation
                        </a>
                        <a href="https://www.ielts.org/for-test-takers/test-format/writing" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            Official Writing Guidelines
                        </a>
                        <a href="https://www.ieltspodcast.com/ielts-writing/" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            IELTS Writing Podcast
                        </a>
                    </div>
                </div>

                <!-- Speaking Skills - Yellow Theme -->
                <div class="resource-category skill-speaking">
                    <div class="category-title">
                        <i class="fas fa-microphone"></i>
                        Speaking Skills
                    </div>
                    <div class="resource-links">
                        <a href="https://www.sparkskytech.com/ielts/ielts-speaking" class="resource-link" target="_blank">
                            <i class="fas fa-comments"></i>
                            IELTS Speaking Practice
                        </a>
                        <a href="https://www.ielts.org/for-test-takers/test-format/speaking" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            Official Speaking Format
                        </a>
                        <a href="https://www.youtube.com/c/IELTSSpeaking" class="resource-link external-link" target="_blank">
                            <i class="fab fa-youtube"></i>
                            IELTS Speaking YouTube
                        </a>
                    </div>
                </div>

                <!-- Vocabulary & Grammar - Purple Theme -->
                <div class="resource-category skill-vocabulary">
                    <div class="category-title">
                        <i class="fas fa-language"></i>
                        Vocabulary & Grammar
                    </div>
                    <div class="resource-links">
                        <a href="https://www.sparkskytech.com/ielts/ielts-vocabulary" class="resource-link" target="_blank">
                            <i class="fas fa-spell-check"></i>
                            IELTS Vocabulary Building
                        </a>
                        <a href="https://www.sparkskytech.com/ielts/ielts-grammar" class="resource-link" target="_blank">
                            <i class="fas fa-grammar"></i>
                            IELTS Grammar Essentials
                        </a>
                        <a href="https://www.cambridge.org/elt/catalogue/subject/custom/item7640665/" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            Cambridge Vocabulary
                        </a>
                    </div>
                </div>

                <!-- Free Resources - Teal Theme -->
                <div class="resource-category skill-resources">
                    <div class="category-title">
                        <i class="fas fa-gift"></i>
                        Free Resources & Tools
                    </div>
                    <div class="resource-links">
                        <a href="https://www.sparkskytech.com/ielts/ielts_free_resources" class="resource-link" target="_blank">
                            <i class="fas fa-download"></i>
                            Free IELTS Resources
                        </a>
                        <a href="https://www.sparkskytech.com/shop/learning-education" class="resource-link" target="_blank">
                            <i class="fas fa-shopping-cart"></i>
                            Educational Digital Products
                        </a>
                        <a href="https://www.examenglish.com/IELTS/" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            Free Practice Tests
                        </a>
                    </div>
                </div>

                <!-- Blog & Tips - Orange Theme -->
                <div class="resource-category skill-blog">
                    <div class="category-title">
                        <i class="fas fa-blog"></i>
                        IELTS Blog & Tips
                    </div>
                    <div class="resource-links">
                        <a href="https://www.sparkskytech.com/blog/ielts_blogs" class="resource-link" target="_blank">
                            <i class="fas fa-newspaper"></i>
                            Latest IELTS Blog Posts
                        </a>
                        <a href="https://www.sparkskytech.com/ielts" class="resource-link" target="_blank">
                            <i class="fas fa-home"></i>
                            IELTS Main Hub
                        </a>
                        <a href="https://ieltsadvantage.com/blog/" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            IELTS Advantage Blog
                        </a>
                    </div>
                </div>

                <!-- Official Resources - Dark Theme -->
                <div class="resource-category skill-official">
                    <div class="category-title">
                        <i class="fas fa-certificate"></i>
                        Official IELTS Resources
                    </div>
                    <div class="resource-links">
                        <a href="https://www.ielts.org/" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt"></i>
                            Official IELTS Website
                        </a>
                        <a href="https://takeielts.britishcouncil.org/" class="resource-link external-link" target="_blank">
                            <i class="fas fa-external-link-alt