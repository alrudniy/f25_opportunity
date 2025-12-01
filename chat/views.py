from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation
from .forms import MessageForm

User = get_user_model()

@login_required
def conversation_list(request):
    conversations = request.user.conversations.prefetch_related('participants').all()
    return render(request, 'chat/conversation_list.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in conversation.participants.all():
        return redirect('chat:conversation_list')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('chat:conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    messages = conversation.messages.select_related('sender').all()
    return render(request, 'chat/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form
    })

@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user == request.user:
        return redirect('dashboard') 

    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    )

    if conversation.exists():
        return redirect('chat:conversation_detail', conversation_id=conversation.first().id)
    else:
        new_conversation = Conversation.objects.create()
        new_conversation.participants.add(request.user, other_user)
        return redirect('chat:conversation_detail', conversation_id=new_conversation.id)
