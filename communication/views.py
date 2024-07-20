from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message
from .forms import MessageForm


@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user)
    return render(request, 'communication/inbox.html', {'messages': received_messages})


@login_required
def sent_messages(request):
    sent_messages = Message.objects.filter(sender=request.user)
    return render(request, 'communication/sent_messages.html', {'messages': sent_messages})


@login_required
def compose_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('inbox')
    else:
        form = MessageForm(user=request.user)
    return render(request, 'communication/compose_message.html', {'form': form})


@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'communication/view_message.html', {'message': message})
