from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm
from django.core.mail import send_mail
from django.contrib import messages


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{form.cleaned_data['from_name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{form.cleaned_data['from_name']}'s comment: {form.cleaned_data['share_message']}"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=form.cleaned_data["from_email"],
                recipient_list=[form.cleaned_data["to_email"]],
            )
            to_mail = form.cleaned_data["to_email"]
            messages.success(
                request, f"{post.title} was successfully sent to {to_mail}"
            )
            return render(
                request, "blog/post/share.html", {"post": post, "form": form}
            )
        messages.error(request, "Error sending mail")
        return render(
            request, "blog/post/share.html", {"post": post, "form": form}
        )

    form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form}
    )
