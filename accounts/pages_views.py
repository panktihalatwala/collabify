from django.shortcuts import render
from django.contrib import messages

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    if request.method == 'POST':
        messages.success(request, "Thanks for reaching out! We'll get back to you within 24 hours.")
    return render(request, 'pages/contact.html')

def faqs(request):
    faqs = [
        {'question': 'What is Collabify?', 'answer': 'Collabify is an influencer marketing platform that connects brands with creators for authentic collaborations. We make it easy to discover, connect, and manage influencer partnerships.'},
        {'question': 'Is Collabify free to use?', 'answer': 'Yes! Collabify is completely free for creators to join and use. Brands can sign up for free and post campaigns. We offer premium plans for advanced analytics and features.'},
        {'question': 'How do I get started as a creator?', 'answer': 'Simply click "Join as Creator", fill in your details, and complete your profile. Add your social media stats, niche, and pricing. Brands will start discovering you right away.'},
        {'question': 'How do I post a campaign as a brand?', 'answer': 'After creating your brand account, go to your Dashboard and click "Create Campaign". Fill in your campaign details, budget, requirements and publish. Creators will start applying immediately.'},
        {'question': 'How does payment work?', 'answer': 'Payments are negotiated directly between brands and creators through our platform. You can discuss rates via our messaging system and set terms before starting a collaboration.'},
        {'question': 'How do I message a creator or brand?', 'answer': 'You can message anyone directly from their profile page or through the Messages section. Real-time chat is available once both parties are connected.'},
        {'question': 'Can I cancel a collaboration?', 'answer': 'Yes. Both brands and creators can cancel a collaboration before work begins. We encourage clear communication through our messaging system to resolve any issues.'},
        {'question': 'How are creators verified?', 'answer': 'Creators verify their social media accounts by linking them to their profile. Our admin team reviews accounts and issues verified badges to authentic, high-quality creators.'},
        {'question': 'What niches are supported?', 'answer': 'We support all major niches including Fashion, Beauty, Fitness, Food, Travel, Tech, Gaming, Lifestyle, Business, Education, Entertainment, Health, Parenting, Finance, and more.'},
        {'question': 'How do I report a fake account?', 'answer': 'Visit the user\'s profile and click the "Report" link at the bottom. Our team reviews all reports within 24 hours and takes action against policy violations.'},
    ]
    return render(request, 'pages/faqs.html', {'faqs': faqs})

def privacy(request):
    sections = [
        {'title': '1. Information We Collect', 'content': 'We collect information you provide directly to us, such as your name, email address, profile information, and social media statistics. We also collect usage data to improve our platform.'},
        {'title': '2. How We Use Your Information', 'content': 'We use the information we collect to provide, maintain, and improve our services, send notifications, process transactions, and communicate with you about your account.'},
        {'title': '3. Information Sharing', 'content': 'We do not sell your personal information. We share information only with your consent, to comply with laws, to protect our rights, or to provide services you have requested.'},
        {'title': '4. Data Security', 'content': 'We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.'},
        {'title': '5. Cookies', 'content': 'We use cookies and similar tracking technologies to track activity on our platform and hold certain information to improve your experience.'},
        {'title': '6. Your Rights', 'content': 'You have the right to access, update, or delete your personal information at any time through your account settings. You may also contact us to exercise these rights.'},
        {'title': '7. Contact Us', 'content': 'If you have questions about this Privacy Policy, please contact us at privacy@collabify.com.'},
    ]
    return render(request, 'pages/privacy.html', {'sections': sections})

def terms(request):
    sections = [
        {'title': '1. Acceptance of Terms', 'content': 'By accessing and using Collabify, you accept and agree to be bound by the terms and provision of this agreement.'},
        {'title': '2. User Accounts', 'content': 'You are responsible for maintaining the confidentiality of your account and password. You agree to accept responsibility for all activities that occur under your account.'},
        {'title': '3. Creator Responsibilities', 'content': 'Creators agree to provide accurate follower and engagement statistics, deliver agreed-upon content on time, and maintain professional conduct with brand partners.'},
        {'title': '4. Brand Responsibilities', 'content': 'Brands agree to provide clear campaign briefs, pay agreed rates promptly, and treat creators with respect. Misleading campaign descriptions are strictly prohibited.'},
        {'title': '5. Prohibited Activities', 'content': 'Users may not use Collabify for any unlawful purpose, to harass others, to post false information, to impersonate others, or to engage in fraudulent activities.'},
        {'title': '6. Payment Terms', 'content': 'Collabify is a marketplace platform. Payment terms are agreed between brands and creators directly. Collabify is not responsible for payment disputes.'},
        {'title': '7. Termination', 'content': 'We may terminate or suspend your account at any time for violations of these terms. You may also delete your account at any time from your account settings.'},
        {'title': '8. Changes to Terms', 'content': 'We reserve the right to modify these terms at any time. We will notify users of significant changes via email or platform notification.'},
    ]
    return render(request, 'pages/terms.html', {'sections': sections})