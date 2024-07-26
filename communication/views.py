from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, Notification
from .forms import MessageForm, ForwardMessageForm
from django.http import HttpResponseForbidden


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
        form = MessageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            Notification.objects.create(user=message.recipient, message=message)
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
        Notification.objects.filter(user=request.user, message=message).update(is_read=True)
    return render(request, 'communication/view_message.html', {'message': message})


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.recipient == request.user or message.sender == request.user:
        message.delete()
        messages.success(request, 'Message deleted successfully.')
    else:
        return HttpResponseForbidden()
    return redirect('inbox')


@login_required
def forward_message(request, message_id):
    original_message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = ForwardMessageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.save()
            Notification.objects.create(user=new_message.recipient, message=new_message)
            messages.success(request, 'Message forwarded successfully.')
            return redirect('inbox')
    else:
        initial_data = {
            'subject': f'Fwd: {original_message.subject}',
            'body': f'\n\n-------- Forwarded Message --------\nFrom: {original_message.sender}\nTo: {original_message.recipient}\nSubject: {original_message.subject}\n\n{original_message.body}',
            'attachment': original_message.attachment
        }
        form = ForwardMessageForm(user=request.user, initial=initial_data)
    return render(request, 'communication/forward_message.html', {'form': form, 'original_message': original_message})


@login_required
def reply_message(request, message_id):
    parent_message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.sender = request.user
            reply.recipient = parent_message.sender
            reply.parent = parent_message
            reply.save()
            Notification.objects.create(user=reply.recipient, message=reply)
            messages.success(request, 'Reply sent successfully.')
            return redirect('inbox')
    else:
        initial_data = {
            'subject': f'Re: {parent_message.subject}',
            'recipient': parent_message.sender,
            'body': f'\n\n-------- Original Message --------\nFrom: {parent_message.sender}\nTo: {parent_message.recipient}\nSubject: {parent_message.subject}\n\n{parent_message.body}'
        }
        form = MessageForm(user=request.user, initial=initial_data)
    return render(request, 'communication/reply_message.html', {'form': form, 'parent_message': parent_message})


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'communication/notifications.html', {'notifications': notifications})
