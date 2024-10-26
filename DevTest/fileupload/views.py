import pandas as pd
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import FileUploadForm

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Read file into a DataFrame
            df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)

            # Generate summary (modify according to your needs)
            summary = df.describe().to_html()  # Simple summary

            # Send email
            email_body = f"Data Summary:\n\n{df.describe().to_string()}"
            send_mail(
                subject='Python Assignment - Your Name',
                message=email_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['tech@themedius.ai']
            )

            return render(request, 'fileupload/summary.html', {'summary': summary})
    else:
        form = FileUploadForm()
    return render(request, 'fileupload/upload.html', {'form': form})
