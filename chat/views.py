from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count
from .models import Conversation
from .forms import MessageForm

User = get_user_model()

@login_required
def conversation_list(request):
    """Display a list of the current user's conversations."""
    conversations = request.user.conversations.all()
    return render(request, 'chat/conversation_list.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    """Display a single conversation thread."""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
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
    
    return render(request, 'chat/conversation_detail.html', {'conversation': conversation, 'form': form})

@login_required
def start_conversation(request, user_id):
    """Start a new conversation with another user."""
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user == request.user:
        return redirect('chat:conversation_list')

    # Find conversation with exactly these two participants.
    conversation = Conversation.objects.annotate(
        p_count=Count('participants')
    ).filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).filter(
        p_count=2
    ).first()

    if conversation:
        return redirect('chat:conversation_detail', conversation_id=conversation.id)
    else:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
        return redirect('chat:conversation_detail', conversation_id=conversation.id)
