from flask import render_template


def render_email(opname, **kwargs):
    subject = render_template(opname+'_subject.txt', **kwargs)
    subject = ' '.join(subject.split())
    html_message = render_template(opname+'_message.html', **kwargs)
    text_message = render_template(opname+'_message.txt', **kwargs)
    return (subject, html_message, text_message)
