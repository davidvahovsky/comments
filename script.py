# from django.utils import timezone
# from random import randint
# from dateutil.relativedelta import relativedelta
# from faker import Faker
# from articles.models import Article
# from articles.models import Comment
#
#
# def create_comments(depth, article, comment, comments):
#     fake = Faker()
#     if not comment:
#         beginning = article.date_created
#     else:
#         beginning = comment.date_created
#     now_comment = beginning
#     for i in range(comments):
#         nick = fake.name()
#         lorem = fake.lorem()
#         body = lorem[:randint(5, 500)]
#         likes = randint(-100, 100)
#         spam = randint(0, 20)
#         comment_pub = now_comment
#         new_comment = Comment(nick=nick, body=body, likes=likes, spam=spam, article=article, comment=comment,
#                               date_created=comment_pub)
#         new_comment.save()
#         if new_comment.comment:
#             comment_id = new_comment.comment.id
#         else:
#             comment_id = None
#         print("ARTICLE: %s, COMMENT: %s, COMMENT PARENT: %s, COMMENT PUBLISHED: %s" %
#               (new_comment.article.id, new_comment.id, comment_id, new_comment.date_created))
#         now_comment = now_comment + relativedelta(hours=randint(0, 2), minutes=randint(0, 59), seconds=randint(0, 59))
#         if depth != 0:
#             create_comments(depth - 1, article, new_comment, randint(0, comments)//2)
#
#
# def fill_db(articles, comments, depth):
#     fake = Faker()
#     now = timezone.now()
#     beginning = now - relativedelta(years=10)
#     now_article = beginning
#     for i in range(articles):
#         author = fake.name()
#         lorem = fake.lorem()
#         title = lorem[:randint(5, 50)]
#         body = fake.lorem()
#         article_pub = now_article
#         article = Article(author=author, title=title, body=body, date_created=article_pub)
#         article.save()
#         print("ARTICLE: %s" % article.title)
#         now_article = now_article + relativedelta(days=randint(0, 2), hours=randint(0, 23),
#                                                   minutes=randint(0, 59), seconds=randint(0, 59))
#         create_comments(depth, article, None, randint(comments//3, comments))
#
#
# fill_db(5, 45, 5)