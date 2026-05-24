import re, sys

def _scan_skip_strings_comments(text):
    pass

def strip_bracketed(text, open_ch, close_ch, only_after_option=False):
    """Remove open..close blocks (string/comment aware). If only_after_option, only
    remove '(' blocks that are part of an 'option (...)...;' statement, consuming to ';'."""
    out=[]; i=0; n=len(text)
    in_line=in_block=in_str=False
    while i<n:
        c=text[i]; two=text[i:i+2]
        if in_line:
            out.append(c); i+=1
            if c=='\n': in_line=False
            continue
        if in_block:
            out.append(c)
            if two=='*/': out.append('/'); i+=2; in_block=False; continue
            i+=1; continue
        if in_str:
            out.append(c)
            if c=='\\' and i+1<n: out.append(text[i+1]); i+=2; continue
            if c=='"': in_str=False
            i+=1; continue
        if two=='//': in_line=True; out.append(two); i+=2; continue
        if two=='/*': in_block=True; out.append(two); i+=2; continue
        if c=='"': in_str=True; out.append(c); i+=1; continue
        if c==open_ch:
            depth=1; i+=1; sstr=False
            while i<n and depth>0:
                cc=text[i]
                if sstr:
                    if cc=='\\': i+=2; continue
                    if cc=='"': sstr=False
                    i+=1; continue
                if cc=='"': sstr=True
                elif cc==open_ch: depth+=1
                elif cc==close_ch: depth-=1
                i+=1
            if out and out[-1]==' ': out.pop()
            continue
        out.append(c); i+=1
    return ''.join(out)

def strip_custom_options(text):
    # Remove 'option (...) ... ;' (parenthesized custom options), keeping 'option name = ...;'.
    out=[]; i=0; n=len(text)
    in_line=in_block=in_str=False
    while i<n:
        if not (in_line or in_block or in_str) and text.startswith('option', i) and (i==0 or not (text[i-1].isalnum() or text[i-1]=='_')):
            j=i+6
            while j<n and text[j] in ' \t': j+=1
            if j<n and text[j]=='(':
                k=j; pdepth=cdepth=bdepth=0; sstr=False
                while k<n:
                    cc=text[k]
                    if sstr:
                        if cc=='\\': k+=2; continue
                        if cc=='"': sstr=False
                        k+=1; continue
                    if cc=='"': sstr=True
                    elif cc=='(': pdepth+=1
                    elif cc==')': pdepth-=1
                    elif cc=='{': cdepth+=1
                    elif cc=='}': cdepth-=1
                    elif cc=='[': bdepth+=1
                    elif cc==']': bdepth-=1
                    elif cc==';' and pdepth==0 and cdepth==0 and bdepth==0:
                        k+=1; break
                    k+=1
                while k<n and text[k] in ' \t': k+=1
                if k<n and text[k]=='\n': k+=1
                while out and out[-1] in ' \t': out.pop()
                i=k; continue
        c=text[i]; two=text[i:i+2]
        if in_line:
            out.append(c); i+=1
            if c=='\n': in_line=False
            continue
        if in_block:
            out.append(c)
            if two=='*/': out.append('/'); i+=2; in_block=False; continue
            i+=1; continue
        if in_str:
            out.append(c)
            if c=='\\' and i+1<n: out.append(text[i+1]); i+=2; continue
            if c=='"': in_str=False
            i+=1; continue
        if two=='//': in_line=True; out.append(two); i+=2; continue
        if two=='/*': in_block=True; out.append(two); i+=2; continue
        if c=='"': in_str=True
        out.append(c); i+=1
    return ''.join(out)

def transform(text):
    text=re.sub(r'^\s*import "logger/options\.proto";\n','',text,flags=re.M)
    text=strip_bracketed(text,'[',']')      # field/enum options [...]
    text=strip_custom_options(text)         # option (...) ... ;
    text=re.sub(r'^package livekit;','package livekit_protocol_ex;',text,flags=re.M)
    text=re.sub(r'^package rpc;','package livekit_protocol_ex.rpc;',text,flags=re.M)
    text=re.sub(r'^package psrpc;','package livekit_protocol_ex.psrpc;',text,flags=re.M)
    text=re.sub(r'\bpsrpc\.','livekit_protocol_ex.psrpc.',text)
    text=re.sub(r'\blivekit\.(?=[A-Z])','livekit_protocol_ex.',text)
    text=re.sub(r'\brpc\.(?=[A-Z])','livekit_protocol_ex.rpc.',text)
    return text

open(sys.argv[2],'w').write(transform(open(sys.argv[1]).read()))
print("transformed",sys.argv[1])
