from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib import messages
from .forms import ContactForm
from .models import ContactInfo, Inquiry


def contact_page(request):
    info = ContactInfo.objects.first()
    # allow pre-filling product via ?product=Product+Name from product detail pages
    initial = {}
    product_q = request.GET.get('product')
    if product_q:
        initial['product'] = product_q

    form = ContactForm(request.POST or None, initial=initial)

    # Get product value for template display
    product_value = initial.get('product', '')
    if request.POST:
        product_value = request.POST.get('product', product_value)

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data

        # Save inquiry to database
        inquiry = Inquiry.objects.create(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            message=data['message'],
            product=data.get('product', ''),
        )

        # Send confirmation email to the user
        try:
            subject = 'We received your inquiry — Computer & CCTV Hub'

            # ─────────────────────────────────────────────────────────────
            # USER CONFIRMATION EMAIL
            # ─────────────────────────────────────────────────────────────
            html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Inquiry Received — Computer & CCTV Hub</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f1f5f9;color:#334155}}
  .wrap{{max-width:600px;margin:32px auto;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08)}}
  .head{{background:#0f2d5e;padding:36px 32px;text-align:center}}
  .head-icon{{width:52px;height:52px;background:rgba(255,255,255,0.1);border-radius:10px;margin:0 auto 18px;display:flex;align-items:center;justify-content:center}}
  .head-icon svg{{width:28px;height:28px}}
  .head h1{{color:#fff;font-size:20px;font-weight:700;margin-bottom:4px;letter-spacing:0.2px}}
  .head p{{color:rgba(255,255,255,0.55);font-size:13px}}
  .badge{{display:inline-flex;align-items:center;gap:6px;margin-top:16px;background:#16a34a;color:#fff;font-size:12px;font-weight:600;padding:5px 14px;border-radius:20px;letter-spacing:0.3px}}
  .badge svg{{width:12px;height:12px}}
  .body{{background:#fff;padding:32px}}
  .body h2{{color:#0f2d5e;font-size:18px;font-weight:700;margin-bottom:8px}}
  .body .intro{{color:#64748b;font-size:14px;line-height:1.7;margin-bottom:24px}}
  .card{{background:#f8fafd;border:0.5px solid #dbe6f5;border-radius:10px;overflow:hidden;margin-bottom:20px}}
  .card-head{{background:#0f2d5e;padding:10px 16px;display:flex;align-items:center;gap:8px}}
  .card-head svg{{width:13px;height:13px}}
  .card-head span{{color:rgba(255,255,255,0.75);font-size:11px;font-weight:700;letter-spacing:0.8px;text-transform:uppercase}}
  .row{{display:flex;justify-content:space-between;align-items:center;padding:11px 16px;border-bottom:0.5px solid #e8eef7}}
  .row:last-child{{border-bottom:none}}
  .row .lbl{{color:#64748b;font-size:13px}}
  .row .val{{color:#0f2d5e;font-size:13px;font-weight:600;background:#eaf1fb;padding:3px 10px;border-radius:5px;max-width:60%;text-align:right;word-break:break-word}}
  .msg-box{{background:#f0f7ff;border-left:3px solid #2563eb;border-radius:0 6px 6px 0;padding:14px 16px;margin-bottom:24px}}
  .msg-lbl{{color:#1e40af;font-size:11px;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;margin-bottom:6px}}
  .msg-box p{{color:#1e3a5f;font-size:14px;line-height:1.7}}
  .divider{{height:0.5px;background:#e2e8f0;margin:20px 0}}
  .help{{color:#94a3b8;font-size:13px;text-align:center}}
  .help a{{color:#2563eb;font-weight:600;text-decoration:none}}
  .foot{{background:#0f2d5e;padding:24px 32px;text-align:center}}
  .foot .brand{{color:#fff;font-size:14px;font-weight:700;margin-bottom:6px}}
  .foot .services{{color:rgba(255,255,255,0.5);font-size:12px;margin-bottom:4px}}
  .foot .copy{{color:rgba(255,255,255,0.3);font-size:11px}}
  @media(max-width:480px){{
    .wrap{{margin:0;border-radius:0}}
    .body{{padding:24px 20px}}
    .head{{padding:28px 20px}}
    .row{{flex-direction:column;align-items:flex-start;gap:6px}}
    .row .val{{max-width:100%;text-align:left}}
  }}
</style>
</head>
<body>
<div class="wrap">
  <div class="head">
    <div class="head-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.8">
        <rect x="2" y="3" width="20" height="14" rx="2"/>
        <path d="M8 21h8M12 17v4"/>
      </svg>
    </div>
    <h1>Computer &amp; CCTV Hub</h1>
    <p>Your trusted technology partner</p>
    <div class="badge">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="20 6 9 17 4 12"/>
      </svg>
      Inquiry received
    </div>
  </div>

  <div class="body">
    <h2>Hello, {data['name']}</h2>
    <p class="intro">
      Thank you for reaching out to us. We have received your inquiry and our
      expert team will respond within <strong>24 hours</strong>.
    </p>

    <div class="card">
      <div class="card-head">
        <svg viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2">
          <path d="M9 11l3 3L22 4"/>
          <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
        </svg>
        <span>Inquiry summary</span>
      </div>
      <div class="row">
        <span class="lbl">Email</span>
        <span class="val">{data['email']}</span>
      </div>
      <div class="row">
        <span class="lbl">Phone</span>
        <span class="val">{data.get('phone', 'Not provided')}</span>
      </div>
      <div class="row">
        <span class="lbl">Product</span>
        <span class="val">{data.get('product', 'General inquiry')}</span>
      </div>
    </div>

    <div class="msg-box">
      <div class="msg-lbl">Your message</div>
      <p>{data['message']}</p>
    </div>

    <div class="divider"></div>
    <p class="help">
      Need immediate help?
      <a href="tel:+1234567890">Call us directly</a>
    </p>
  </div>

  <div class="foot">
    <p class="brand">Computer &amp; CCTV Hub</p>
    <p class="services">Laptops &middot; CCTV Systems &middot; Repairs &middot; Tech Solutions</p>
    <p class="copy">&copy; 2026 All rights reserved</p>
  </div>
</div>
</body>
</html>'''

            text_content = f'''Hello {data['name']},

Thank you for contacting Computer & CCTV Hub! We have received your inquiry
and will respond within 24 hours.

Inquiry summary:
  Email:   {data['email']}
  Phone:   {data.get('phone', 'Not provided')}
  Product: {data.get('product', 'General inquiry')}
  Message: {data['message']}

Best regards,
Computer & CCTV Hub Team'''

            msg = EmailMultiAlternatives(subject, text_content, None, [data['email']])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

            # ─────────────────────────────────────────────────────────────
            # OWNER NOTIFICATION EMAIL
            # ─────────────────────────────────────────────────────────────
            if info and info.email:
                owner_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>New inquiry — Computer & CCTV Hub</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f1f5f9;color:#334155}}
  .wrap{{max-width:600px;margin:32px auto;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08)}}
  .urgent-bar{{background:#7f1d1d;padding:8px 0;text-align:center}}
  .urgent-bar span{{color:#fca5a5;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase}}
  .head{{background:#1a0505;padding:32px 32px 28px;text-align:center}}
  .head-icon{{width:52px;height:52px;background:rgba(239,68,68,0.15);border-radius:10px;margin:0 auto 18px;display:flex;align-items:center;justify-content:center}}
  .head-icon svg{{width:28px;height:28px}}
  .head h1{{color:#fff;font-size:20px;font-weight:700;margin-bottom:4px}}
  .head p{{color:rgba(255,255,255,0.45);font-size:13px}}
  .badge-alert{{display:inline-flex;align-items:center;gap:6px;margin-top:16px;background:#dc2626;color:#fff;font-size:12px;font-weight:600;padding:5px 14px;border-radius:20px;letter-spacing:0.3px}}
  .badge-alert svg{{width:12px;height:12px}}
  .body{{background:#fff;padding:32px}}
  .alert-chip{{display:inline-flex;align-items:center;gap:6px;background:#fef2f2;color:#b91c1c;border:0.5px solid #fca5a5;font-size:12px;font-weight:600;padding:5px 12px;border-radius:20px;margin-bottom:16px;letter-spacing:0.3px}}
  .alert-chip svg{{width:12px;height:12px}}
  .card{{background:#fdf8f8;border:0.5px solid #fecaca;border-radius:10px;overflow:hidden;margin-bottom:20px}}
  .card-head{{background:#7f1d1d;padding:10px 16px;display:flex;align-items:center;gap:8px}}
  .card-head svg{{width:13px;height:13px}}
  .card-head span{{color:rgba(255,180,180,0.85);font-size:11px;font-weight:700;letter-spacing:0.8px;text-transform:uppercase}}
  .row{{display:flex;justify-content:space-between;align-items:center;padding:11px 16px;border-bottom:0.5px solid #fee2e2}}
  .row:last-child{{border-bottom:none}}
  .row .lbl{{color:#64748b;font-size:13px}}
  .row .val{{color:#7f1d1d;font-size:13px;font-weight:600;background:#fef2f2;padding:3px 10px;border-radius:5px;max-width:60%;text-align:right;word-break:break-word}}
  .msg-box{{background:#fffbeb;border-left:3px solid #d97706;border-radius:0 6px 6px 0;padding:14px 16px;margin-bottom:24px}}
  .msg-lbl{{color:#92400e;font-size:11px;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;margin-bottom:6px}}
  .msg-box p{{color:#451a03;font-size:14px;line-height:1.7}}
  .btn-row{{display:flex;gap:10px;margin-top:4px}}
  .btn{{flex:1;display:block;text-align:center;padding:12px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none}}
  .btn-reply{{background:#0f2d5e;color:#fff}}
  .btn-call{{background:#fff;color:#0f2d5e;border:1.5px solid #0f2d5e}}
  .foot{{background:#0f2d5e;padding:24px 32px;text-align:center}}
  .foot .brand{{color:#fff;font-size:14px;font-weight:700;margin-bottom:6px}}
  .foot .services{{color:rgba(255,255,255,0.5);font-size:12px;margin-bottom:4px}}
  .foot .copy{{color:rgba(255,255,255,0.3);font-size:11px}}
  @media(max-width:480px){{
    .wrap{{margin:0;border-radius:0}}
    .body{{padding:24px 20px}}
    .head{{padding:24px 20px 20px}}
    .btn-row{{flex-direction:column}}
    .row{{flex-direction:column;align-items:flex-start;gap:6px}}
    .row .val{{max-width:100%;text-align:left}}
  }}
</style>
</head>
<body>
<div class="wrap">
  <div class="urgent-bar">
    <span>Action required — respond within 24 hours</span>
  </div>

  <div class="head">
    <div class="head-icon">
    </div>
    <h1>New customer inquiry</h1>
    <p>Lead from {data['name']}</p>
    <div class="badge-alert">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
      </svg>
      New lead
    </div>
  </div>

  <div class="body">
    <div class="alert-chip">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      New lead waiting for a response
    </div>

    <div class="card">
      <div class="card-head">
        <svg viewBox="0 0 24 24" fill="none" stroke="rgba(255,160,160,0.9)" stroke-width="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          <circle cx="12" cy="7" r="4"/>
        </svg>
        <span>Customer details</span>
      </div>
      <div class="row">
        <span class="lbl">Name</span>
        <span class="val">{data['name']}</span>
      </div>
      <div class="row">
        <span class="lbl">Email</span>
        <span class="val">{data['email']}</span>
      </div>
      <div class="row">
        <span class="lbl">Phone</span>
        <span class="val">{data.get('phone', 'Not provided')}</span>
      </div>
      <div class="row">
        <span class="lbl">Product</span>
        <span class="val">{data.get('product', 'General inquiry')}</span>
      </div>
    </div>

    <div class="msg-box">
      <div class="msg-lbl">Customer message</div>
      <p>{data['message']}</p>
    </div>

    <div class="btn-row">
      <a href="mailto:{data['email']}" class="btn btn-reply">Reply by email</a>
      <a href="tel:{data.get('phone', '')}" class="btn btn-call">Call customer</a>
    </div>
  </div>

  <div class="foot">
    <p class="brand">Computer &amp; CCTV Hub</p>
    <p class="services">Customer success team &middot; 24/7 support</p>
    <p class="copy">&copy; 2026 All rights reserved</p>
  </div>
</div>
</body>
</html>'''

                owner_text = f'''NEW INQUIRY FROM {data['name'].upper()}
Action required — respond within 24 hours.

Name:    {data['name']}
Email:   {data['email']}
Phone:   {data.get('phone', 'Not provided')}
Product: {data.get('product', 'General inquiry')}
Message: {data['message']}'''

                owner_msg = EmailMultiAlternatives(
                    f'New inquiry: {data["name"]} — Computer & CCTV Hub',
                    owner_text,
                    None,
                    [info.email]
                )
                owner_msg.attach_alternative(owner_html, 'text/html')
                owner_msg.send()

            messages.success(request, 'Your message has been sent! Check your email for confirmation.')
        except Exception as e:
            messages.success(request, 'Your message has been saved! We will contact you soon.')

        return redirect('contact:contact_page')

    return render(request, 'contact/contact.html', {
        'info': info,
        'form': form,
        'product_value': product_value,
    })