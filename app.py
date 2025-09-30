from flask import Flask, request, render_template_string, url_for, render_template_string
import datetime
import json
import subprocess
from flask import Blueprint, request, send_file
from PIL import Image
import os
import uuid

app = Flask(__name__)

# Sample data
products = [
"ডিশ কভার ১৪ সেমি - লাল",
"ডিশ কভার ২০ সেমি - লাল",
"ডিশ কভার ২৫ সেমি - লাল",
"ডিশ কভার ৩২ সেমি - লাল",
"ডিশ কভার ৩৮ সেমি - লাল",
"এ.বি.সি চেয়ার- লাল",
"ব্ল্যাংকেট বক্স - ট্রান্সপারেন্ট",
"বাবল মগ - নীল",
"বাবল মগ - গোলাপি",
"বুলেট মগ ১.৫লি - নীল",
"বুলেট মগ ১.৫লি - লাল",
"বুলেট মগ ২.৫লি - নীল",
"বুলেট মগ ২.৫লি - লাল",
"বুলেট মগ ২লি - নীল",
"বুলেট মগ ২লি - লাল",
"কেইনো পেপার বাস্কেট - ঈগল ব্রাউন",
"চালুনি বড় - লাল",
"চালুনি মাঝারি - লাল",
"চালুনি ছোট - লাল",
"চেরি জগ ৩.৫লি - ট্রান্সপারেন্ট নীল",
"চেরি জগ ৩.৫লি - ট্রান্সপারেন্ট লাল",
"ক্লিন আপ ডাস্ট প্যান",
"কনটেইনার- ফ্রেস্কো স্কয়ার-৪ পিস সেট - ট্রান্সপারেন্ট",
"কসমোস জগ ৩.৫লি - পার্ল পিঙ্ক ও পার্ল পিঙ্ক",
"কসমোস জগ ৩.৫লি - ট্রান্সপারেন্ট ও লাল",
"ক্রাউন জগ ২.৩লি - ট্রান্সপারেন্ট",
"ক্রাউন জগ ২.৩লি - ট্রান্সপারেন্ট নীল",
"ক্রাউন জগ ২.৩লি - ট্রান্সপারেন্ট রোজ",
"কিউট ওয়াটার বোতল ২০০ এম.এল - অ্যাসর্টেড",
"কিউট ওয়াটার বোতল ২০০ এম.এল - ট্রান্সপারেন্ট ও গোলাপি",
"কিউট বোতল ২০০ এম.এল",
"কিউট বোতল ৪০০ এম.এল",
"ডিয়ার বেবি পটি - লাল",
"ডাস্ট কিপার পেপার বাস্কেট - নীল",
"ডাস্ট কিপার পেপার বাস্কেট - লাল",
"ডাস্ট কিপার পেপার বাস্কেট মাঝারি - নীল",
"ডাস্ট কিপার পেপার বাস্কেট মাঝারি - লাল",
"ইজি ব্যাগ - নীল",
"ইজি স্টুল মাঝারি - টিয়া সবুজ",
"ইজি স্টুল মাঝারি - টিউলিপ সবুজ",
"এলিগেন্ট ডাস্ট প্যান - লাল",
"এলিগেন্ট ডাস্ট প্যান - এস.এম নীল",
"ফ্যামিলি বাস্কেট - ক্রিম ও ব্রাউন",
"ফ্যামিলি বাস্কেট - পার্ল পিঙ্ক ও পার্ল পিঙ্ক",
"ফ্লিপ অ্যান্ড ক্লিন ডাস্ট বিন ১০লি",
"ফ্লিপ অ্যান্ড ক্লিন ডাস্ট বিন ১৬লি",
"ফ্লিপ অ্যান্ড ক্লিন ডাস্ট বিন ৪লি",
"ফ্রেস্কো মিনি আরটিজি কনটেইনার - ট্রান্স- ২৬০মিলি",
"হামান ডিস্তা - ঈগল ব্রাউন",
"হামান ডিস্তা - লাল",
"হ্যান্ড ফ্যান - নীল",
"হ্যান্ড ফ্যান - লাল",
"বাথ টাব বড় - ব্লু",
"বাথ টাব বড় - পিঙ্ক",
"বাথ টাব ছোট - লাল",
"হোলি রেহাল - অ্যাসর্টেড",
"হোলি রেহাল - লাল",
"আইভরি ওয়াটার বোতল ৬০০ মি.লি - টি.আর পিঙ্ক",
"আইভরি ওয়াটার বোতল ৮০০ মি.লি - টি.আর পিঙ্ক",
"জলকান্ডা - অ্যাসর্টেড",
"কিপ বেটার বক্স ৩ পিস সেট - লাইট ব্লু",
"কিপ বেটার বক্স ৩ পিস সেট - পার্ল পিঙ্ক",
"লিলি ওয়াশিং নেট ১৮ সেমি - লাল",
"লিলি ওয়াশিং নেট ২৪ সেমি - লাল",
"লিলি ওয়াশিং নেট ২৮ সেমি - লাল",
"লিলি ওয়াশিং নেট ৩৪ সেমি - লাল",
"লিলি ওয়াশিং নেট ৩৭ সেমি - লাল",
"লিলি ওয়াশিং নেট ৪২ সেমি - লাল",
"লিলি ওয়াশিং নেট ৪৮ সেমি - লাল",
"লিরা জার ১৬০ মি.লি - অ্যাসর্টেড",
"ললি আইসক্রিম মেকার - সাদা",
"লোটাস সল্ট জার - ট্রান্স",
"মারবেল বোতল ৪৫০ মি.লি - অ্যাসর্টেড",
"মারবেল বোতল ৪৫০ মি.লি - লেইম গ্রিন",
"মারবেল বোতল ৫৫০ মি.লি - অ্যাসর্টেড",
"মারবেল বোতল ৫৫০ মি.লি - ডিপ পিঙ্ক",
"মারবেল বোতল ৫৫০ মি.লি - লেইম গ্রিন",
"মারবেল বোতল ৬৫০ মি.লি - অ্যাসর্টেড",
"মারবেল বোতল ৬৫০ মি.লি - ডিপ পিঙ্ক",
"মারবেল বোতল ৬৫০ মি.লি - লেইম গ্রিন",
"মার্লো বোতল ৪৫০ মি.লি - অ্যাসর্টেড",
"মার্লো বোতল ৬০০ মি.লি - অ্যাসর্টেড",
"মাইক্রোওয়েভ কনটেইনার ৩পিস সেট(বিগ,মিডি,স্মল)-পিচ",
"মাইক্রোওয়েভ কনটেইনার ৩পিস সেট(বিগ,মিডি,স্মল)-পিংক",
"মাম পট",
"মৌসুমী র‍্যাক ৪ স্টেপ - লাল ও সাদা",
"মৌসুমী র‍্যাক ৪ স্টেপ - এস.এম ব্লু ও সাদা",
"মুভিং বাস্কেট উইথ নোহা জার - লাল",
"মুভিং শার্ট হ্যাঙ্গার ৪১সেমি ৬ পিস সেট - লাল",
"মুভিং শার্ট হ্যাঙ্গার ৪১সেমি ৬ পিস সেট- এস.এম ব্লু",
"মুভিং বাস্কেট উইথ ৬ পিস জার",
"মাল্টিপারপাস কনটেইনার ৪ পিস সেট (৩,৫,৭,১০লি) - প্রিন্টেড",
"মাল্টিপারপাস কনটেইনার ১০লি - প্রিন্টেড",
"মাল্টিপারপাস কনটেইনার ১৫লি - প্রিন্টেড",
"মাল্টিপারপাস কনটেইনার ২০লি - প্রিন্টেড",
"মাল্টিপারপাস কনটেইনার ২৫লি - প্রিন্টেড",
"মাল্টিপারপাস কনটেইনার ৩লি - প্রিন্টেড",
"মাল্টিপারপাস কনটেইনার ৫লি - প্রিন্টেড",
"মাল্টিপারপাস কনটেইনার ৭লি - প্রিন্টেড",
"মাল্টিপারপাস আরটিজি বক্স-লাইট ব্লু",
"মাল্টিপারপাস আরটিজি বক্স-লাইম গ্রিন",
"মাল্টিপারপাস আরটিজি বক্স-লাল",
"মাল্টিপারপাস আরটিজি বক্স-হলুদ",
"মাল্টিপারপাস স্কয়ার বক্স-লাইট ব্লু",
"মাল্টিপারপাস স্কয়ার বক্স-লাইম গ্রিন",
"নোহা জার ১৩০ মি.লি - অ্যাসর্টেড",
"নোহা জার ৩০০ মি.লি - অ্যাসর্টেড",
"নোহা জার ৪২৫ মি.লি - অ্যাসর্টেড",
"ওভাল বাকেট ১০লি - লাল",
"ওভাল বাকেট ১৫লি - লাল",
"ওভাল বাকেট ২০লি - লাল",
"ওভাল বাকেট ২৫লি - লাল",
"ওভাল বাকেট ৩০লি - লাল",
"ওভাল বাকেট ৩৫লি - লাল",
"ওভাল বাকেট ৫লি - লাল",
"ওভাল বাকেট ৮লি - লাল",
"ওভাল অয়েল জার - ট্রান্স গোল্ডেন",
"পেট সল্ট জার",
"প্যান-ডাস্ট-ব্লু",
"প্যান-ডাস্ট-রেড",
"পেট বাস্কেট - ক্রিম ও ব্রাউন",
"প্লাস্টিক কুলা বড় - লাল",
"প্লাস্টিক কুলা ছোট",
"পাওয়ার স্টুল হাই - লাল",
"পাওয়ার স্টুল হাই - টিউলিপ গ্রিন",
"পাওয়ার স্টুল হাই - উড",
"পাওয়ার স্টুল মিডিয়াম - লাল",
"পাওয়ার স্টুল মিডিয়াম - টিউলিপ গ্রিন",
"পিউর আরটিজি কনটেইনার ৩৭০০ মিলি",
"পিউর আরটিজি কনটেইনার ৫০০০ মিলি",
"পিউর আরটিজি কনটেইনার ৮০০০ মিলি",
"রেইনবো কনটেইনার অভাল ৪ পিস সেট ১.১,০.৫৯,০.৩৪,০.১৮লি-টি.আর",
"রেহাল - লাল",
"রাইস ওয়াশিং নেট ৩০ সেমি - সায়ান ব্লু",
"রাইস ওয়াশিং নেট ৩০ সেমি - লাল",
"রাইস ওয়াশিং নেট ৩৫ সেমি - সায়ান ব্লু",
"রাইস ওয়াশিং নেট ৩৫ সেমি - লাল",
"রাইস ওয়াশিং নেট ৪০ সেমি - সায়ান ব্লু",
"রাইস ওয়াশিং নেট ৪০ সেমি - লাল",
"রোমান ওয়াল র‍্যাক - লাইট ব্লু",
"রোমান ওয়াল র‍্যাক - লাল ও সাদা",
"সালাড কাটিং বোর্ড - সাদা",
"সালাড কাটিং বোর্ড বড় - সাদা",
"স্কুল টিফিন বক্স - পিংক",
"শার্ট হ্যাঙ্গার ৪১সেমি ৬ পিস সেট- লাল",
"শার্ট হ্যাঙ্গার ৪১সেমি ৬ পিস সেট- এস.এম ব্লু",
"শু র‍্যাক ৪ স্টেপ (বিগ) - স্যান্ডাল উড",
"শপিং বাস্কেট - লাল",
"স্লিম ডাস্ট প্যান - লাল",
"স্মার্ট কিচেন র‍্যাক মিনি - ঈগল ব্রাউন",
"স্মার্ট কিচেন র‍্যাক মিনি - টু কালার",
"স্টোর কনটেইনার ৩পিস সেট - ট্রান্স",
"সানফ্লাওয়ার ওয়াটার বোতল ৬০০ মিলি - অ্যাসর্টেড",
"সুপার বোল ১০লি - লাল",
"সুপার বোল ১৫লি - লাল",
"সুপার বোল ১৮লি - লাল",
"সুপার বোল ২০লি - লাল",
"সুপার বোল ২৫লি - লাল",
"সুপার বোল ২৮লি - লাল",
"সুপার বোল ৩০লি - লাল",
"সুপার বোল ৩লি - লাল",
"সুপার বোল ৫লি - লাল",
"সুপার বোল ৮লি - লাল",
"সুপার বাকেট ১০লি - লাল",
"সুপার বাকেট ১২লি - লাল",
"সুপার বাকেট ১৫লি - লাল",
"সুপার বাকেট ১৮লি - লাল",
"সুপার বাকেট ২০লি - লাল",
"সুপার বাকেট ২২লি - লাল",
"সুপার বাকেট ২৫লি - লাল",
"সুপার বাকেট ৩০লি - লাল",
"সুপার বাকেট ৪লি - লাল",
"সুপার বাকেট ৮লি - লাল",
"সুপার র‍্যাক ৪ স্টেপ - লাল",
"সুপার র‍্যাক ৪ স্টেপ - এস.এম ব্লু",
"টিউলিপ ফেন্স র‍্যাক ৪ স্টেপ টু কালার - নীল",
"টিউলিপ ফেন্স র‍্যাক ৪ স্টেপ টু কালার - লাল",
"টু কালার ডিসেন্ট র‍্যাক",
"টু কালার প্রেসিডেন্ট স্টুল - স্যান্ডাল উড ও লাল",
"টু কালার প্রেসিডেন্ট স্টুল - টিউলিপ গ্রিন ও লাল",
"টু কালার প্রেসিডেন্ট স্টুল হাই - স্যান্ডাল উড ও লাল",
"টু কালার প্রেসিডেন্ট স্টুল হাই - টিউলিপ গ্রিন ও লাল",
"টু কালার প্রেসিডেন্ট স্টুল মিডিয়াম-স্যান্ডাল উড ও লাল",
"টু কালার প্রেসিডেন্ট স্টুল মিডিয়াম-টিউলিপ গ্রিন ও লাল",
"উনা জার ২.৫লি - অ্যাসর্টেড",
"উনা জার ২লি - অ্যাসর্টেড",
"ইউনিক জগ ১.৮৫লি - ট্রান্স ব্লু",
"ভেজিটেবল ওয়াশিং নেট ২৬ সেমি - লাল",
"ভেজিটেবল ওয়াশিং নেট ৩০ সেমি - লাল",
"ভেজিটেবল ওয়াশিং নেট ৩৩ সেমি - লাল",
"ভেজিটেবল ওয়াশিং নেট ৩৪ সেমি - লাল",
"ভেজিটেবল ওয়াশিং নেট ৩৭ সেমি - লাল",
"ভেজিটেবল ওয়াশিং নেট ৪২ সেমি - লাল",
"ভেজিটেবল ওয়াশিং নেট ৪৮ সেমি - লাল",
"ভেজিটেবল ওয়াশিং নেট ৫৬ সেমি - লাল",
"ভেজিটেবল ওয়াশিং নেট ৫৬ সেমি - এস.এম ব্লু",
"ভেনাস রাউন্ড টিফিন বক্স - নীল",
"ওয়েস্টেজ বিন - লাইট গ্রে",
"ওয়াটার পট ২.২৫লি - নীল",
"ওয়াটার পট ইকোনমি উইথ নেট ২.২৫লি - লাল",
"ওয়েভ বাকেট ১০লি - লাল",
"ওয়েভ বাকেট ৫লি - এস.এম ব্লু",
"ওয়েভ বাকেট উইথ লিড ১৫লি - লাল",
"হিটার জগ (পি.পি) ১.৮লি",
"হিটার জগ (পি.পি) ২.৫লি",
"অ্যাকমি রাউন্ড ওয়াল ক্লক - গোল্ডেন",
"এয়ার টাইট রাউন্ড কনটেইনার ৩ পিস সেট - ট্রান্স",
"আজিনা মেপল ডিজিট রাউন্ড ওয়াল ক্লক - ব্লু",
"আজিনা মেপল ডিজিট রাউন্ড ওয়াল ক্লক - অরেঞ্জ",
"আজিনা মেপল ডিজিট স্কোয়ার ওয়াল ক্লক - ব্লু",
"আজিনা মেপল ডিজিট স্কোয়ার ওয়াল ক্লক - অরেঞ্জ",
"আজিনা মোশন এলইডি ডিজিটাল ওয়াল ক্লক",
"আজিনা মোশন এলইডি ডিজিটাল ওয়াল ক্লক - গ্রিন",
"আজিনা মোশন এলইডি ডিজিটাল ওয়াল ক্লক মিডিয়াম - রেড",
"আটলান্টা ওয়াটার জগ ৩লি - অ্যাসসোর্টেড",
"আটা চালনি বড় - রেড",
"আটা চালতি ছোট - রেড",
"বিউটি বক্স - ট্রান্স পিঙ্ক",
"বিউটি ক্লথ ক্লিপ ১০ পিস সেট - অ্যাসসোর্টেড",
"বেলি জগ ২.৩লি - ট্রান্স",
"বেলি জগ ২.৩লি - ট্রান্স ব্লু",
"বেলি জগ ২.৩লি - ট্রান্স পার্পল",
"কেইনো লন্ড্রি বাস্কেট স্মল - ঈগল ব্রাউন",
"কেইনো আরটিজি বাস্কেট উইথ লিড ১৫লি - অ্যাসসোর্টেড",
"কেইনো আরটিজি বাস্কেট উইথ লিড ১৫লি - গ্রে",
"কেইনো আরটিজি বাস্কেট উইথ লিড ২.৩লি - অ্যাসসোর্টেড",
"কেইনো আরটিজি বাস্কেট উইথ লিড ২৮লি - অ্যাসসোর্টেড",
"কেইনো আরটিজি বাস্কেট উইথ লিড ৬.৭৫লি - অ্যাসসোর্টেড",
"ক্যামেলিয়া গামলা ৩৫লি - রেড",
"ক্যাপ্টেন ক্লিন মাজুনি ১২ পিস সেট",
"ক্যাসিনো ওয়াল ক্লক উইদাউট ডিজিট রাউন্ড-গ্রিন",
"চায়না ঝাড়ু - লাইম গ্রিন",
"চায়না ঝাড়ু - অরেঞ্জ",
"চায়না ঝাড়ু - ইয়েলো",
"কসমস জগ ২.৭৫লি - পার্ল পিঙ্ক ও পার্ল পিঙ্ক",
"কসমস জগ ২.৭৫লি - ট্রান্স ও রেড",
"ক্রিস্টাল সাবান কেস-অ্যাসসোর্টেড",
"সাইক্লোন চার্জিং ফ্যান - পিচ",
"ডেইজি আইস ট্রে উইথ কাভার - লাইট ব্লু",
"ডেইজি আইস ট্রে উইথ কাভার - রেড",
"ডাল চামুচ - স্যান্ডাল উড",
"ডিলাক্স মাল্টি পারপাস ক্রেট-ব্লু",
"ডিলাক্স স্টুল - অফ হোয়াইট",
"ডিলাক্স ওয়াল ক্লক রাউন্ড উইদাউট ডিজিট - গোল্ডেন",
"ডিলাক্স ওয়াল ক্লক রাউন্ড উইদাউট ডিজিট - সিলভার",
"ডিলাক্স ওয়াল ক্লক রাউন্ড উইথ ডিজিট - গোল্ডেন",
"ড্রিঙ্কো মগ - ট্রান্স ও লাইম গ্রিন",
"ড্রিঙ্কো মগ - ট্রান্স ও ইয়েলো",
"ইজি আইস ক্রিম মেকার - হোয়াইট",
"এলিট অয়েল ডিজ্পেন্সার ৪৫০ এমএল",
"এলিট অয়েল ডিজ্পেন্সার ৫৫০ এমএল",
"ইংলিশ ডিশ রাক - রেড",
"ইংলিশ ডিশ রাক মিনি - রেড",
"ফিশ বাস্কেট - ব্লু",
"ফিশ বাস্কেট - টিউলিপ গ্রিন",
"ফ্লেক্সি সাবান কেস-অ্যাসসোর্টেড",
"ফ্লোর ক্লিন ফুল ঝাড়ু - এমএস",
"ফ্লোর ক্লিন ফুল ঝাড়ু - এসএস",
"ফ্লাওয়ার ডাল মিক্সচার - স্যান্ডাল উড",
"ফোল্ডিং বাস্কেট",
"ফ্রিজার বোতল ক্লাসিক ২লি - অ্যাসসোর্টেড",
"ফ্রেশ পেপার বাস্কেট বড় - রেড",
"ফ্রেশ পেপার বাস্কেট বড় - এসএম ব্লু",
"ফ্রেশ পেপার বাস্কেট মিডিয়াম - রেড",
"ফ্রেশ পেপার বাস্কেট মিডিয়াম - এসএম ব্লু",
"ফ্রেশ পেপার বাস্কেট ছোট - রেড",
"ফ্রেশ পেপার বাস্কেট ছোট - এসএম ব্লু",
"গ্লাসকো জার ১১৫০ এমএল",
"গ্লাসকো জার ১৫৫০ এমএল",
"গ্লাসকো জগ ২.৩লি - ট্রান্স","গ্লাসকো জাগ ২.৩লি - ট্রান্স ব্লু",
"গ্লাসকো জগ ২.৩লি - ট্রান্স রোজ",
"হ্যামলেট আরও ওয়াল ক্লক - রেড",
"হ্যামলেট আরও ওয়াল ক্লক-লাইট ব্লু",
"হ্যাপি কিড্ডো পিসি ওয়াটার বটল ৪৫০ এমএল - ট্রান্স পিঙ্ক",
"হারি স্ট্যান্ড ৩মিমি লার্জ - জি",
"হারি স্ট্যান্ড ৩মিমি মিডিয়াম - জি",
"হারি স্ট্যান্ড ৪মিমি লার্জ - জি",
"হারি স্ট্যান্ড ৪মিমি মিডিয়াম - জি",
"হারি স্ট্যান্ড আরও উইদাউট স্টপার ২ পিস সেট ৪ মিমি মিডিয়াম-৩আর",
"হারি স্ট্যান্ড আরও উইথ স্টপার ২ পিস সেট ৪মিমি মিডিয়াম-৩আর",
"হেভি রেহাল-রেড",
"হেভি রেহাল-রয়াল ব্লু",
"হর্স বেবি পটি - রেড",
"আইভরি অয়েল জার ১০০০ এমএল",
"জেসমিন ক্লথ ক্লিপ ১২ পিস সেট উইথ রোপ",
"জেসমিন ক্লথ ক্লিপ ৮ পিস সেট - অ্যাসসোর্টেড",
"জেসমিন ক্লথ ক্লিপ-১২ পিস সেট-অ্যাসসোর্টেড",
"জর্দি ওয়াল ক্লক রাউন্ড- ব্ল্যাক",
"জুসি জগ ১.৬লি - ট্রান্স",
"কিচেন টুল শর্ট - রেড",
"কিতো ওয়াল ক্লক স্কোয়ার-ব্ল্যাক",
"কিতো ওয়াল ক্লক স্কোয়ার-গোল্ডেন",
"লাবনি স্টোরেজ কনটেইনার ১৫লি - পীচ",
"লাবনি স্টোরেজ কনটেইনার ১৫লি - পিঙ্ক",
"লিফ সাবান কেস - অ্যাসসোর্টেড",
"লোগান ক্লাসিক ওয়াল ক্লক-ব্লু-স্টেপ",
"লুসি মগ ৫০০ এমএল - অ্যাসসোর্টেড",
"লাক্সারি সাবান কেস - অ্যাসসোর্টেড",
"মেকআপ মিক্সচার সেট",
"ম্যাসন ওয়াল ক্লক ওভাল - রেড",
"ম্যাসন ওয়াল ক্লক ওভাল- ব্ল্যাক",
"মেক্কা রেহাল - রেড",
"মীম ওয়াটার বোতল ৬০০ এমএল",
"মেটাল বাথরুম শেলফ",
"মেটাল মেশ ট্রলি ৩ লেয়ার",
"মেটাল মেশ ইউটিলিটি কার্ট বিগ -হোয়াইট",
"মেটাল মেশ ইউটিলিটি কার্ট স্মল -ব্ল্যাক",
"মেটাল শু রাক ৩ স্টেপ -ব্ল্যাক",
"মেটাল শু রাক ৪ স্টেপ - হোয়াইট",
"মেটাল স্পাইস রাক ২ স্টেপ",
"মেটাল ওয়াল শেলফ",
"মিমো ওভাল টিফিন বক্স - পিঙ্ক",
"মিনা কনটেইনার বড় - হোয়াইট ও রেড",
"মিনা কনটেইনার মিডিয়াম - হোয়াইট ও রেড",
"মিনা কনটেইনার ছোট - হোয়াইট & রেড","মিনা ওয়াটার বটল ৪৫০ এমএল - ট্রান্স হানি",
"মিনি বোল ১৫০০ এমএল - রেড",
"মিনি বোল ৬২০ এমএল - রেড",
"মিরর ডিলাক্স - এস এম ব্লু",
"মিরর ডিলাক্স -পার্ল পিঙ্ক",
"মডার্ন অর্গানাইজার",
"মৌসুমি জগ ২.২লি উইদাউট প্যাক - ট্রান্স",
"ন্যানসি ক্রপ বাস্কেট বিগ - হবি ব্রাউন",
"ন্যানসি ক্রপ বাস্কেট স্মল - হবি ব্রাউন",
"নোটবুক ওয়াটার বটল ৩৫০ এমএল",
"অলিভিয়া অয়েল জার ৭৫০এমএল",
"অলিভার ওয়াটার বোতল ৫০০ এমএল-অ্যাসসোর্টেড",
"অলিভার ওয়াটার বোতল ৯০০ এমএল-অ্যাসসোর্টেড",
"অলিভিয়া মগ - গ্রে ও হোয়াইট",
"অলিভিয়া মগ - পিস্তা গ্রিন ও হোয়াইট",
"অলিভিয়া মগ - রেড ও হোয়াইট",
"অরবিট আরটি জি ওয়াল ক্লক",
"অরবিট আরটি জি ওয়াল ক্লক উইথ ডিজিট-ব্ল্যাক",
"প্যাসিফিক বেবি চেয়ার",
"প্যাসিফিক রাউন্ড স্টুল বড় - রেড",
"প্যাসিফিক রাউন্ড স্টুল ছোট - রেড",
"প্যাসিফিক রাউন্ড স্টুল ছোট - এসএম ব্লু",
"প্যাসিফিক সু ৫ স্টেপ - রেড",
"প্যাসিফিক সু রাক ৪ স্টেপ - রেড",
"প্যাসিফিক ওয়াটারl বোতল ৫০০ এমএল - ট্রান্স গ্রিন",
"প্যাসিফিক ওয়াটার বটল ৭০০ এমএল - ট্রান্স গ্রিন",
"প্যানোরামা ওভাল মিরর - অ্যাসসোর্টেড",
"প্রেয়ার অ্যাকসেসরিজ শেলফ - মেটাল",
"প্রিটি ওয়াটার বটল উইথ বেল্ট ৪০০ এমএল - ব্লু",
"প্রিটি ওয়াটার বটল উইথ বেল্ট ৪০০ এমএল-পিঙ্ক",
"প্রিটি ওয়াটার বটল উইথ বেল্ট ৪০০ এমএল-পার্পল",
"প্রিটি ওয়াটার বটল উইথ বেল্ট ৪০০ এমএল-ইয়েলো",
"প্রোমো আরটি জি টিফিন বক্স - রেড",
"আরএফএল স্লটেড টার্নার - গ্রে",
"আরএফএল সলিড টার্নার - গ্রে",
"আরএফএল স্প্যাটুলা টার্নার - গ্রে",
"রাপিড মশকিউটো কিলিং ব্যাট - ব্লু",
"রাপিড মশকিউটো কিলিং ব্যাট - লাইম গ্রিন",
"রাপিড মশকিউটো কিলিং ব্যাট - ম্যাজেন্টা",
"রিফ্রেশু সাবান কেস-অ্যাসসোর্টেড",
"রাউন্ড মাল্টিপারপাস স্ট্যান্ড - মেটাল",
"রাউন্ড মাল্টিপারপাস স্ট্যান্ড ছোট - মেটাল",
"রাউন্ড স্টুল - টি.জি",
"আরটি জি কাটলারি স্ট্যান্ড - মেটাল",
"রুবি ক্লথ ক্লিপ ১০ পিস সেট - অ্যাসসোর্টেড",
"রুবি ক্লথ ক্লিপ-১২ পিস সেট-অ্যাসসোর্টেড",
"রুবি অয়েল জার ৪৫০ এমএল",
"সামীরা জগ রাউন্ড ১.৮লি - ট্রান্স রেড",
"শিউলি মগ ১.৫লি - এস এম ব্লু",
"শিউলি মগ ১.৬লি - ব্লু",
"শিউলি মগ ১.৬লি - রেড",
"শিউলি মগ ২লি - রেড",
"শিউলি মগ ২লি - এস এম ব্লু",
"সুলোভ সুপার বালতি ১২লি - ব্ল্যাক",
"সুলোভ সুপার বালতি ৮লি - ব্ল্যাক",
"স্লিম প্যাডল বিন ৬.৬লি - টিউলিপ গ্রিন",
"স্লিম ওয়াটার বটল ৩৫০এমএল উইথ রিং",
"স্মার্ট রাক ৪ স্টেপ - রেড ও হোয়াইট",
"স্মার্ট রাক ৪ স্টেপ প্রিন্টেড - রেড ও হোয়াইট",
"স্মার্ট রাক ৫ স্টেপ - রেড ও হোয়াইট",
"স্মাইলি কিডো ওয়াটার বোতল ৪৫০ এমএল-ট্রু ব্লু",
"স্পার্ক ওয়াটার বোতল ৫৫০ এমএল - অ্যাসসোর্টেড",
"স্পার্ক ওয়াটার বোতল ৭০০ এমএল - অ্যাসসোর্টেড",
"স্কয়ার প্যাডল বিন ৩০লি - সিলভার",
"স্কয়ার স্টুল মিডিয়াম - রেড",
"স্কয়ার স্টুল মিডিয়াম - উড",
"স্ট্যান্ডার্ড মিনি রাক - রেড ও হোয়াইট",
"স্টাইল ফেন্স রাক ৪ স্টেপ (বিগ) - রেড ও হোয়াইট",
"স্টাইল ফেন্স রাক ৪ স্টেপ (বিগ) - এস এম ব্লু ও হোয়াইট",
"স্টাইল ফেন্স রাক ৫ স্টেপ (বিগ) - রেড ও হোয়াইট",
"স্টাইলিশ শার্ট হ্যাঙ্গার ০৬ পিস সেট - ব্লু",
"স্টাইলিশ শার্ট হ্যাঙ্গার ০৬ পিস সেট - রেড",
"সানকাস্ট ওয়াল ক্লক রাউন্ড উইথ পেপার প্রিন্ট - কফি",
"সানকাস্ট ওয়াল ক্লক স্কোয়ার উইথ পেপার প্রিন্ট - কফি",
"সানফ্লাওয়ার গ্লাস স্ট্যান্ড - রেড",
"সানফ্লাওয়ার ওয়াল ক্লক - ব্ল্যাক",
"সানফ্লাওয়ার ওয়াল ক্লক-গোল্ডেন",
"সুপার ওয়াল ক্লক রাউন্ড - ব্ল্যাক",
"সুপার ওয়াল ক্লক উইথ ডিজিট রাউন্ড - গোল্ডেন",
"সুইট বেবি বাথ টাব - পিঙ্ক",
"তাখযিন কনটেইনার ১০লি - পিঙ্ক",
"তাখযিন কনটেইনার ৪ পিস সেট - পীচ",
"তাখযিন কনটেইনার ৪ পিস সেট - পিঙ্ক",
"তাখযিন কনটেইনার ৫লি - পীচ",
"তাখযিন কনটেইনার ৭লি - পীচ",
"তাখযিন কনটেইনার ৭লি - পিঙ্ক",
"টিনি অর্গানাইজার - লাইট পিঙ্ক",
"টিনি অর্গানাইজার ৫ স্টেপ - লাইট পিঙ্ক",
"থাই জার ১.৫লি - অ্যাসসোর্টেড",
"থাই জার ২.৫লি-অ্যাসসোর্টেড",
"থাই জার ২লি - অ্যাসসোর্টেড",
"থাই জার ৮০০ এমএল",
"থান্ডার ওয়াটার বোতল ৫৫০ এমএল",
"থান্ডার ওয়াটার বোতল ১০০০ এমএল",
"ট্র্যাশ বিন ১২০লি",
"ট্র্যাশ বিন ১২০লি - অ্যাসসোর্টেড",
"ট্র্যাশ বিন ১২০লি-ব্ল্যাক",
"ট্র্যাশ বিন ১২০লি-রেড",
"ট্র্যাশ বিন ১২০লি-টি.জি",
"ট্র্যাশ বিন ১২০লি-ইয়েলো",
"ট্র্যাশ বিন ২৪০লি",
"ট্র্যাশ বিন ২৪০লি - অ্যাসসোর্টেড",
"ট্র্যাশ বিন ২৪০লি উইথ প্যাডল-রেড",
"ট্র্যাশ বিন ২৪০লি-রেড",
"ট্র্যাশ বিন ২৪০লি-উইথ প্যাডল","ট্র্যাশ বিন ৬০লি",
"ট্র্যাশ বিন ৬০লি - অ্যাসসোর্টেড",
"টিউলিপ গামলা ১০লি - রেড",
"টিউলিপ গামলা ১৫লি - রেড",
"টিউলিপ গামলা ২০লি - রেড",
"টিউলিপ গামলা ২৫লি - রেড",
"টিউলিপ গামলা ২লি - রেড",
"টিউলিপ গামলা ৫লি - রেড",
"টিউলিপ বালতি ১০লি - রেড",
"টিউলিপ বালতি ১২লি - রেড",
"টিউলিপ বালতি ১৬লি - রেড",
"টিউলিপ বালতি ২০লি - রেড",
"টিউলিপ বালতি ২৫লি - রেড",
"টিউলিপ বালতি ৩০লি - রেড",
"টিউলিপ বালতি ৩৫লি - রেড",
"টিউলিপ বালতি ৩লি - রেড",
"টিউলিপ বালতি ৫লি - রেড",
"টিউলিপ বালতি ৮লি - রেড",
"টিউলিপ বালতি লিড ১০লি - রেড",
"টিউলিপ বালতি লিড ১২লি - রেড",
"টিউলিপ বালতি লিড ১৬লি - রেড",
"টিউলিপ বালতি লিড ২০লি - রেড",
"টিউলিপ বালতি লিড ২৫লি - রেড",
"টিউলিপ বালতি লিড ৩০লি - রেড",
"টিউলিপ বালতি লিড ৩৫লি - রেড",
"টিউলিপ বালতি লিড ৩লি - রেড",
"টিউলিপ বালতি লিড ৫লি - রেড",
"টিউলিপ বালতি লিড ৮লি- রেড",
"টিউলিপ শাড়ি হ্যাঙ্গার ৬ পিস সেট-রেড",
"টিউলিপ ওয়াল ক্লক রাউন্ড - ব্লু টি-১",
"টিউলিপ ওয়াল ক্লক রাউন্ড -ব্ল্যাক",
"টিউন ওয়াল ক্লক রাউন্ড - ব্ল্যাক",
"টিউন ওয়াল ক্লক উইথ ডিজিট রাউন্ড-ব্লু",
"টিউন ওয়াল ক্লক উইথ ডিজিট রাউন্ড-রেড",
"টিউন ওয়াল ক্লক উইথ ডিজিট রাউন্ড-সিলভার-রেড হ্যান্ড",
"টিউন ওয়াল ক্লক উইথ ডিজিট আরও-সিলভার-সিলভার হ্যান্ড-ব",
"টুর্বান স্কোয়ার কার্ভ ওয়াল ক্লক-ব্লু",
"টুর্বান স্কোয়ার কার্ভ ওয়াল ক্লক-ম্যাজেন্টা",
"টুর্বান স্কোয়ার কার্ভ ওয়াল ক্লক-অরেঞ্জ",
"টুর্বান স্কোয়ার কার্ভ ওয়াল ক্লক-ইয়েলো",
"টু কালার ক্লথ ক্লিপ -১২ পিস সেট",
"টু কালার ম্যাজিক স্টুল হাই",
"টু কালার ম্যাজিক স্টুল মিডিয়াম",
"টু কালার ম্যাজিক স্টুল ছোট",
"টু কালার নেট ৩১ সেমি - রেড",
"টু কালার নেট ৩৪ সেমি - রেড",
"টু কালার নেট ৩৭ সেমি - রেড",
"ঊনা ওয়াটার বটল ১২০০ এমএল-অ্যাসসোর্টেড",
"ইউনিক বেলচা - রেড",
"ইউনিক বেলচা - এস এম ব্লু",
"ভিআইপি স্টুল - রেড",
"বদনা ২.৯লি - রেড"]


# Customer data format reverted to Name:Address
customer_data = [
"বি.ডি.আর:নওগাঁ সদর",
"শুভ:নওগাঁ সদর",
"এমদাদ:নওগাঁ সদর",
"মান্নান:নওগাঁ সদর",
"বাবু সার্ভিস:নওগাঁ সদর",
"রিয়া:নওগাঁ সদর",
"দিলিপ:নওগাঁ সদর",
"সুকুমার দাদা:নওগাঁ সদর",
"কেয়া:নওগাঁ সদর",
"শরিফ:নওগাঁ সদর",
"রিংকু:নওগাঁ সদর",
"অনন্যা:নওগাঁ সদর",
"কুমিল্লা:নওগাঁ সদর",
"ফারহানা:নওগাঁ সদর",
"বলাই:নওগাঁ সদর",
"রাশেদ ভাই:নওগাঁ সদর",
"বিকাশ দাদা:নওগাঁ সদর",
"হারুন:নওগাঁ সদর",
"কর্ণফুলী:নওগাঁ সদর",
"দিলিপ পোদ্দার:নওগাঁ সদর",
"বাবু চাচা:তিলকপুর",
"আত্তাব:তিলকপুর",
"ভাই ভাই:তিলকপুর",
"রাশেদ:তিলকপুর",
"পাপ্পু:তিলকপুর",
"নয়ন:তিলকপুর",
"বাঁধন:তিলকপুর",
"ইব্রাহিম:তিলকপুর",
"মৌমিতা বড় ভাই:তিলকপুর",
"মৌমিতা:তিলকপুর",
"জুয়ের:তিলকপুর",
"সজিব:মাদারমোল্লা",
"ভান্দারি:মাদারমোল্লা",
"হাজী:রানীনগর",
"প্রত্যয়:রানীনগর",
"রাজ:রানীনগর",
"সাহা:রানীনগর",
"নীথি:রানীনগর",
"ভি.আই.পি:রানীনগর",
"হান্ডেট প্লাস:রানীনগর",
"রাইসা:রানীনগর",
"অন্নিমা:রানীনগর",
"সৌরভ:নগর ব্রীজ",
"রুবেল:কুবলাতলী",
"আইসা বেদিন:কুবলাতলী",
"ভাই ভাই:কুবলাতলী",
"সপন:কুজাইল",
"সরদার:ভবানীপুর",
"কর্মকার:ভবানীপুর",
"মা হার্ডওয়্যার:ভবানীপুর",
"ভাই ভাই:ভবানীপুর",
"রাধাঁ:ভবানীপুর",
"সরদার:বেতগাড়ী",
"ফারজানা:বেতগাড়ী",
"সাহেব আলী:বেতগাড়ী",
"আশা:বেতগাড়ী",
"রাহুল:বেতগাড়ী",
"মোসাদ্দেক:বেতগাড়ী",
"পাবনা:আত্রাই",
"রিয়াদ:আত্রাই",
"সাফিন:আত্রাই",
"বারিক:আত্রাই",
"ঐশী:আত্রাই",
"ইলা:আত্রাই",
"জোৎস্না:আত্রাই",
"গোলাপ:বান্দাইখাড়া",
"জোবায়ের:বান্দাইখাড়া",
"রুইস:বান্দাইখাড়া",
"পাবনা:বান্দাইখাড়া",
"রেজাউল:সুতিহাট",
"বিসমিল্লাহ:বদলগাছি"
]

# Parse customer data (reverted to original logic)
customers = []
customer_addresses = {}
for data in customer_data:
    if ':' in data:
        name, address = data.split(':', 1)
        customers.append(name)
        customer_addresses[name] = address
    else:
        customers.append(data)
        customer_addresses[data] = ""

addresses = list(set(customer_addresses.values()))

# Company details
company_name = "মেসার্স সবুর প্লাস্টিক হাউস"
company_owner = "প্রো: মোঃ সবুর হোসেন"
company_address = "পুরাতন কাঠহাটি, নওগাঁ"
company_phone = "০১৯৭০২৩৬২৪৮"
company_email = "০১৮৪৪৫৬৫৭৫১"
company_email2 = "০১৮৪৪৫৬৫৭১৯"
left_logo_url = "https://sunxfire.alwaysdata.net/KFFmvP2.png"
right_logo_url = "https://iili.io/KFFyO42.png"

# Custom Jinja2 filter for Bangla digits
def to_bangla_digits(value):
    bangla_digits = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')
    return str(value).translate(bangla_digits)

app.jinja_env.filters['to_bangla_digits'] = to_bangla_digits

# Modernized form template with Orange/Red color scheme
form_template = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>মেমো জেনারেটর</title>
   <link href="{{ url_for('static', filename='notosansbengali.css') }}" rel="stylesheet">
<link href="{{ url_for('static', filename='tailwind.min.css') }}" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans Bengali', sans-serif; background: #fef7ed; }
        .suggestions { 
            position: absolute; 
            background: white; 
            border: 1px solid #fdba74; 
            max-height: 150px; 
            overflow-y: auto; 
            z-index: 10; 
            width: 100%; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .suggestion-item { 
            padding: 8px; 
            cursor: pointer; 
        }
        .suggestion-item:hover { 
            background-color: #fed7aa; 
        }
        @media print { 
            .no-print { display: none; } 
        }
        .header-gradient {
            background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
        }
        .section-border {
            border-left: 4px solid #ea580c;
        }
        /* Column specific colors */
        .column-product { background: #fed7aa !important; }
        .column-quantity { background: #fdba74 !important; }
        .column-price { background: #fb923c !important; }
        .column-total { background: #ea580c !important; color: white !important; }
        .column-action { background: #dc2626 !important; color: white !important; }
    </style>
</head>
<body class="bg-orange-50">
    <div class="container mx-auto p-4 max-w-4xl">
      <header class="header-gradient shadow rounded-lg p-4 mb-6 border-2 border-orange-500">
    <div class="flex items-center justify-between">
        <img src="{{ left_logo_url }}" alt="বাম লোগো" class="w-24 h-auto">

        <div class="text-center">
            <h1 class="text-3xl font-bold text-orange-800">{{ company_name }}</h1>
            <p class="text-lg text-orange-900">{{ company_owner }}</p>
            <p class="text-sm text-orange-800">{{ company_address }}</p>
            <p class="text-base text-orange-700 font-semibold">
                ফোন(ডিলার): {{ company_phone }} |
                ফোন(প্যাসিফিক): {{ company_email }} |
                ফোন(প্যাসিফিক): {{ company_email2 }}
            </p>
        </div>

        <img src="{{ right_logo_url }}" alt="ডান লোগো" class="w-24 h-auto">
    </div>
</header>

       <div class="bg-orange-50 shadow rounded-lg p-4 mb-6 section-border">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="md:col-span-2">
            <label class="block text-sm font-medium text-orange-900">গ্রাহকের নাম</label>
            <div class="relative">
                <input type="text" id="customerName" class="mt-1 block w-full border-orange-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500 bg-orange-25" autocomplete="off" aria-autocomplete="list">
                <div id="customer-suggestions" class="suggestions hidden"></div>
            </div>
        </div>
        <div>
            <label class="block text-sm font-medium text-orange-900">মেমো নম্বর</label>
            <p id="invoiceNo" class="mt-1 block w-full border-orange-300 rounded-md shadow-sm p-2 bg-orange-100 text-orange-900">{{ invoice_no|to_bangla_digits }}</p>
        </div>
        <div>
            <label class="block text-sm font-medium text-orange-900">তারিখ</label>
            <input type="date" id="date" value="{{ today }}" class="mt-1 block w-full border-orange-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500 bg-orange-25">
        </div>
        <div class="md:col-span-2">
            <label class="block text-sm font-medium text-orange-900">ঠিকানা</label>
            <div class="relative">
                <input type="text" id="customerAddress" class="mt-1 block w-full border-orange-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500 bg-orange-25" autocomplete="off" aria-autocomplete="list">
                <div id="address-suggestions" class="suggestions hidden"></div>
            </div>
        </div>
    </div>
</div>

        <div class="bg-orange-50 shadow rounded-lg p-4 mb-6 no-print section-border">
            <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
                <div class="relative md:col-span-2">
                    <label class="block text-sm font-medium text-orange-900">পণ্য</label>
                    <input type="text" id="searchBox" placeholder="পণ্য অনুসন্ধান..." class="mt-1 block w-full border-orange-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500 bg-orange-25" autocomplete="off" aria-autocomplete="list">
                    <div id="product-suggestions" class="suggestions hidden"></div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-orange-900">পরিমাণ</label>
                    <input type="number" id="price" placeholder="পরিমাণ" step="0.01" min="0" class="mt-1 block w-full border-orange-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500 bg-orange-25">
                </div>
                <div>
                    <label class="block text-sm font-medium text-orange-900">মূল্য</label>
                    <input type="number" id="qty" placeholder="মূল্য" step="1" min="0" class="mt-1 block w-full border-orange-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500 bg-orange-25">
                </div>
                <div>
                    <label class="block text-sm font-medium text-orange-900">একক</label>
                    <select id="unit" class="mt-1 block w-full border-orange-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500 bg-orange-25">
                        <option value="">পিস</option>
                        <option value="D">ডজন</option>
                        <option value="S">সেট</option>
                    </select>
                </div>
            </div>
            <div class="mt-4">
                <button onclick="addItem()" class="w-full bg-orange-600 text-white py-2 px-4 rounded-md hover:bg-orange-700 focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 transition duration-200 font-semibold">যোগ করুন</button>
            </div>
        </div>

        <div class="bg-orange-50 shadow rounded-lg p-4 section-border">
            <table class="w-full border-collapse">
                <thead>
                    <tr>
                        <th class="border border-orange-600 p-2 text-white column-product">পণ্যের নাম</th>
                        <th class="border border-orange-600 p-2 text-white column-quantity">পরিমাণ</th>
                        <th class="border border-orange-600 p-2 text-white column-price">মূল্য</th>
                        <th class="border border-orange-600 p-2 text-white column-total">মোট টাকা</th>
                        <th class="border border-orange-600 p-2 text-white column-action no-print">ক্রিয়া</th>
                    </tr>
                </thead>
                <tbody id="memoTable"></tbody>
                <tfoot>
                    <tr class="bg-orange-200">
                        <td colspan="3" class="border border-orange-400 p-2 font-bold text-orange-900">সর্বমোট</td>
                        <td id="subtotal" class="border border-orange-400 p-2 font-bold text-orange-900 column-total">০</td>
                        <td class="border border-orange-400 p-2 no-print column-action"></td>
                    </tr>
                </tfoot>
            </table>
        </div>
        
        <div class="bg-orange-50 shadow rounded-lg p-4 mt-6 no-print section-border">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <label class="block text-sm font-medium text-orange-900">ডিসকাউন্ট (%)</label>
                    <input type="number" id="discount" name="discount" placeholder="ডিসকাউন্ট (%)" step="0.01" min="0" max="100" class="mt-1 block w-full border-orange-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500 bg-orange-25">
                </div>
                <div>
                    <label class="block text-sm font-medium text-orange-900">আগের বাকি</label>
                    <input type="number" id="previousDue" placeholder="আগের বাকি" step="0.01" min="0" class="mt-1 block w-full border-orange-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500 bg-orange-25">
                </div>
                <div>
                    <label class="block text-sm font-medium text-orange-900">মোট বিল</label>
                    <p id="grandTotal" class="mt-1 block w-full border-orange-300 rounded-md shadow-sm p-2 bg-orange-100 text-orange-900">০</p>
                </div>
            </div>
            <div class="mt-4">
                <label for="notes" class="block text-sm font-medium text-orange-900">ফেরত</label>
                <textarea id="notes" name="notes" rows="3" class="mt-1 block w-full border-orange-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500 bg-orange-25" placeholder="ফেরত সম্পর্কিত নোট লিখুন..."></textarea>
            </div>
        </div>

        <form method="post" action="/generate" class="mt-6">
            <input type="hidden" name="customer" id="customerHidden">
            <input type="hidden" name="address" id="addressHidden">
            <input type="hidden" name="date" id="dateHidden">
            <input type="hidden" name="items" id="itemsHidden">
            <input type="hidden" name="invoice_no" id="invoiceNoHidden">
            <input type="hidden" name="discount" id="discountHidden">
            <input type="hidden" name="notes" id="notesHidden">
            <input type="hidden" name="previous_due" id="previousDueHidden">
            <button type="submit" onclick="prepareForm()" class="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition duration-200 font-semibold no-print">মেমো তৈরি ও মুদ্রণ</button>
        </form>
    </div>

    <script>
        const products = {{ products|tojson }};
        const customers = {{ customers|tojson }};
        const customerAddresses = {{ customer_addresses|tojson }};
        const addresses = {{ addresses|tojson }};
        let items = [];

        // Convert to Bangla digits
        const toBanglaDigits = (number) => {
            const banglaDigits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
            return number.toString().replace(/\d/g, d => banglaDigits[d]);
        };

        // Show suggestions
        const suggest = (input, suggestionsDiv, list, isCustomer = false) => {
            const value = input.value.toLowerCase();
            suggestionsDiv.innerHTML = '';
            suggestionsDiv.classList.add('hidden');
            if (value) {
                const suggestions = list.filter(item => item.toLowerCase().includes(value));
                if (suggestions.length) {
                    suggestionsDiv.classList.remove('hidden');
                    suggestions.forEach(s => {
                        const div = document.createElement('div');
                        div.className = 'suggestion-item';
                        div.textContent = s;
                        div.setAttribute('tabindex', '0');
                        div.addEventListener('click', () => selectSuggestion(input, suggestionsDiv, s, isCustomer));
                        div.addEventListener('keypress', (e) => {
                            if (e.key === 'Enter') selectSuggestion(input, suggestionsDiv, s, isCustomer);
                        });
                        suggestionsDiv.appendChild(div);
                    });
                }
            }
        };

        // Handle suggestion selection
        const selectSuggestion = (input, suggestionsDiv, value, isCustomer) => {
            input.value = value;
            suggestionsDiv.classList.add('hidden');
            if (isCustomer) {
                document.getElementById('customerAddress').value = customerAddresses[value] || '';
            }
            const nextInput = isCustomer ? 'customerAddress' : input.nextElementSibling?.id || 'price';
            document.getElementById(nextInput)?.focus();
        };

        // Add item to table
        const addItem = () => {
            const item = document.getElementById('searchBox').value;
            const price = parseFloat(document.getElementById('price').value) || 0;
            const qty = parseFloat(document.getElementById('qty').value) || 0;
            const unit = document.getElementById('unit').value;

            if (!item || price <= 0 || qty <= 0) {
                alert('অনুগ্রহ করে বৈধ পণ্য, পরিমাণ এবং মূল্য লিখুন');
                return;
            }

            items.push({ item, price, qty, unit, total: price * qty });
            updateTable();
            document.getElementById('searchBox').value = '';
            document.getElementById('price').value = '';
            document.getElementById('qty').value = '';
            document.getElementById('unit').value = 'P';
            document.getElementById('searchBox').focus();
        };

        // Remove item
        const removeItem = (index) => {
            items.splice(index, 1);
            updateTable();
        };

        // Edit item
        const editItem = (index) => {
            const newPrice = prompt('নতুন পরিমাণ লিখুন:', toBanglaDigits(items[index].price));
            const newQty = prompt('নতুন মূল্য লিখুন:', toBanglaDigits(items[index].qty));
            if (newPrice !== null && !isNaN(newPrice) && newPrice > 0) {
                items[index].price = parseFloat(newPrice);
            }
            if (newQty !== null && !isNaN(newQty) && newQty > 0) {
                items[index].qty = parseFloat(newQty);
            }
            items[index].total = items[index].price * items[index].qty;
            updateTable();
        };

        // Update table
        const updateTable = () => {
            const tableBody = document.getElementById('memoTable');
            tableBody.innerHTML = '';
            let subtotal = 0;

            items.forEach((item, index) => {
                subtotal += item.total;
                const row = document.createElement('tr');
                row.className = 'hover:bg-orange-100';
                row.innerHTML = `
                    <td class="border border-orange-300 p-2 text-orange-900 column-product">${item.item}</td>
                    <td class="border border-orange-300 p-2 text-orange-900 column-quantity">${toBanglaDigits(item.price.toFixed(2))}</td>
                    <td class="border border-orange-300 p-2 text-orange-900 column-price">${toBanglaDigits(item.qty)} (${item.unit})</td>
                    <td class="border border-orange-300 p-2 text-orange-900 font-semibold column-total">${toBanglaDigits(item.total.toFixed(2))}</td>
                    <td class="border border-orange-300 p-2 no-print column-action">
                        <button onclick="editItem(${index})" class="text-white hover:text-orange-200 mr-2" aria-label="Edit item">✏️</button>
                        <button onclick="removeItem(${index})" class="text-white hover:text-orange-200" aria-label="Remove item">❌</button>
                    </td>`;
                tableBody.appendChild(row);
            });

            document.getElementById('subtotal').textContent = toBanglaDigits(subtotal.toFixed(2));
            updateGrandTotal();
        };

        // Update grand total based on discount and previous due
        const updateGrandTotal = () => {
            const subtotal = items.reduce((sum, item) => sum + item.total, 0);
            const discountPercent = parseFloat(document.getElementById('discount').value) || 0;
            const previousDue = parseFloat(document.getElementById('previousDue').value) || 0; // Read from input

            const discountAmount = (subtotal * discountPercent) / 100;
            const totalAfterDiscount = subtotal - discountAmount;
            const grandTotal = totalAfterDiscount + previousDue;

            document.getElementById('grandTotal').textContent = toBanglaDigits(grandTotal.toFixed(2));
        };

        // Generate invoice number
        const getInvoiceNumber = () => {
            let num = localStorage.getItem('invoiceNo') || 1000;
            num = parseInt(num) + 1;
            localStorage.setItem('invoiceNo', num);
            return toBanglaDigits(num);
        };

        // Prepare form for submission
        const prepareForm = () => {
            document.getElementById('customerHidden').value = document.getElementById('customerName').value;
            document.getElementById('addressHidden').value = document.getElementById('customerAddress').value;
            document.getElementById('dateHidden').value = document.getElementById('date').value;
            document.getElementById('itemsHidden').value = JSON.stringify(items);
            document.getElementById('invoiceNoHidden').value = document.getElementById('invoiceNo').textContent;
            document.getElementById('discountHidden').value = document.getElementById('discount').value;
            document.getElementById('notesHidden').value = document.getElementById('notes').value;
            document.getElementById('previousDueHidden').value = document.getElementById('previousDue').value;
        };

        // Event listeners
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('invoiceNo').textContent = getInvoiceNumber();
            document.getElementById('discount').addEventListener('input', updateGrandTotal);
            document.getElementById('previousDue').addEventListener('input', updateGrandTotal); // Added listener for due input

            const inputs = [
                { id: 'searchBox', suggestions: 'product-suggestions', list: products },
                { id: 'customerName', suggestions: 'customer-suggestions', list: customers, isCustomer: true },
                { id: 'customerAddress', suggestions: 'address-suggestions', list: addresses }
            ];

            inputs.forEach(({ id, suggestions, list, isCustomer }) => {
                const input = document.getElementById(id);
                const suggestionsDiv = document.getElementById(suggestions);
                input.addEventListener('input', () => suggest(input, suggestionsDiv, list, isCustomer));
                input.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        const nextInput = id === 'searchBox' ? 'price' : id === 'price' ? 'qty' : id === 'qty' ? 'unit' : 'customerAddress';
                        if (typeof nextInput === 'string') document.getElementById(nextInput)?.focus();
                    }
                });
            });

            document.addEventListener('click', (e) => {
                if (!e.target.closest('.suggestions') && !e.target.closest('input')) {
                    document.querySelectorAll('.suggestions').forEach(s => s.classList.add('hidden'));
                }
            });
        });
    </script>
</body>
</html>
"""

# MODIFIED MEMO TEMPLATE WITH SEPARATE COLUMN COLORS
memo_template = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>মেমো</title>
    <link href="{{ url_for('static', filename='notosansbengali.css') }}" rel="stylesheet">
<link href="{{ url_for('static', filename='tailwind.min.css') }}" rel="stylesheet">
<script src="{{ url_for('static', filename='html2canvas.min.js') }}"></script>
    <style>
        :root {
            --header-top-margin: 0px;
            --header-bottom-margin: 0px;
            --company-name-bottom-margin: 0px;
            --border-width: 2px;
        }

        @font-face {
            font-family: 'MyCustomFont';
            src: url('/static/Font/bn1.ttf') format('truetype');
            font-weight: normal;
            font-style: normal;
        }
        body { 
            font-family: 'MyCustomFont', sans-serif; 
            background: #fef7ed; 
            margin: 0;
            padding: 2px;
        }
        
        .a4-paper { 
            width: 2480px;
            height: 3508px;
            background: white; 
            padding: var(---top-margin) 0px 0px 0px;
            box-sizing: border-box; 
            border: 2px solid #ea580c; 
            margin: auto; 
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        #capture-container {
            position: absolute;
            left: -9999px;
            top: 0;
        }
        
        header {
            margin-bottom: var(--header-bottom-margin);
            background: linear-gradient(135deg, #86FFFE 0%, #86FFFE 100%);
            padding: 0px 0px;
            border-radius: 8px;
            border: 2px solid #000000;
        }

        header h1 { 
            font-size: 120px;
            font-weight: 700;
            color: #FF6900;
            margin: 0 0 var(--company-name-bottom-margin) 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        header p { 
            margin: 4px 0;
            font-size: 100px;
            color: #000000;
            font-weight: 600;
        }
        header .phone-info { 
            font-size: 90px; 
            color: #000000;
        }
        .logo { width: 260px; height: auto; }

        .invoice-info {
            background: #B4F9FF;
            padding: 0px;
            border-radius: 6px;
            border: 2px solid #000000;
            margin: 0px 0;
        }

        .invoice-info p {
            margin: 8px 0;
            font-size: 110px;
            color: #000000;
        }

        table { 
            border-collapse: collapse; 
            width: 100%; 
            background: white;
        }
        
        /* Column specific colors for memo */
        .column-product-header { 
            background: #FF1818 !important;
            color: white !important;
            border: var(--border-width) solid #ea580c !important;
        }
        .column-quantity-header { 
            background: #FF1818 !important;
            color: white !important;
            border: var(--border-width) solid #ea580c !important;
        }
        .column-price-header { 
            background: #FF1818 !important;
            color: white !important;
            border: var(--border-width) solid #ea580c !important;
        }
        .column-total-header { 
            background: #FF1818 !important;
            color: white !important;
            border: var(--border-width) solid #ea580c !important;
        }
        
        .column-product-cell { 
            background: #FDFFD7 !important;
            border: var(--border-width) solid #f97316 !important;
        }
        .column-quantity-cell { 
            background: #FEF3F9 !important;
            border: var(--border-width) solid #f97316 !important;
        }
        .column-price-cell { 
            background: #FDF8CE !important;
            border: var(--border-width) solid #f97316 !important;
        }
        .column-total-cell { 
            background: #E9F8FF !important;
            border: var(--border-width) solid #f97316 !important;
        }
        
        table th, table td { 
            padding: 0px 0px;
            text-align: center; 
            vertical-align: middle;
            word-wrap: break-word;
            line-height: 1.4;
            font-weight: 700;
        }
        
        table th {
            font-size: var(--header-font-size);
        }
        table td {
            font-size: var(--cell-font-size);
            height: 150px;
        }
        table td:first-child {
            text-align: left;
        }

        table tfoot td {
            font-size: var(--footer-font-size);
            font-weight: 200;
            background: #D8FFAE;
            color: #000000;
            border: var(--border-width) solid #000000;
        }
        
        .controls {
            position: fixed; 
            top: 20px; 
            right: 20px; 
            background: #fff7ed;
            padding: 20px; 
            border-radius: 8px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000; 
            min-width: 250px;
            border: 2px solid #fdba74;
        }
        
        .control-group { margin-bottom: 15px; }
        .control-group label { 
            display: block; 
            font-weight: 700; 
            margin-bottom: 5px; 
            font-size: 14px; 
            color: #7c2d12; 
        }
        
        .control-group select, .control-group input {
            width: 100%; 
            padding: 8px 12px; 
            border: 1px solid #fdba74;
            border-radius: 4px; 
            font-size: 14px; 
            box-sizing: border-box;
            background: #fffbeb;
        }
        
        @media print { .no-print { display: none !important; } }
        
        .font-small { 
            --header-font-size: 67px; --cell-font-size: 90px; --footer-font-size: 95px; 
        }
        .font-medium { 
            --header-font-size: 67px; --cell-font-size: 100px; --footer-font-size: 110px; 
        }
        .font-large { 
            --header-font-size: 67px; --cell-font-size: 115px; --footer-font-size: 120px; 
        }
        
        /* Print button styling */
        #printMemo {
            background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 28px;
            cursor: pointer;
            padding: 25px 50px;
            box-shadow: 0 4px 6px rgba(234, 88, 12, 0.3);
            transition: all 0.3s ease;
        }
        
        #printMemo:hover {
            background: linear-gradient(135deg, #c2410c 0%, #9a3412 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(234, 88, 12, 0.4);
        }
        
        .notes-section {
            background: #fef3c7;
            padding: 30px;
            border-radius: 6px;
            border: 2px solid #f59e0b;
            margin-top: 20px;
            font-size: 110px;
            color: #92400e;
        }
    </style>
</head>
<body>
    <div style="text-align: center; margin: 50px 0;" class="no-print">
        <button id="printMemo" style="padding: 25px 50px; background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%); color: white; border: none; border-radius: 6px; font-size: 28px; cursor: pointer; box-shadow: 0 4px 6px rgba(234, 88, 12, 0.3);">
            🖨️ মেমো ডাউনলোড করুন
        </button>
    </div>

    <div class="controls no-print">
        <h3 style="margin-top: 0; font-size: 16px; color: #7c2d12;">কাস্টমাইজেশন</h3>
        
        <div class="control-group">
            <label for="headerTopMargin">Top Margin (px): <span id="headerTopMarginValue">20</span></label>
            <input type="range" id="headerTopMargin" min="0" max="300" value="0" oninput="updateHeaderSpacing()">
        </div>
        <div class="control-group">
            <label for="headerBottomMargin">Space Below Header (px): <span id="headerBottomMarginValue">25</span></label>
            <input type="range" id="headerBottomMargin" min="0" max="300" value="0" oninput="updateHeaderSpacing()">
        </div>
        <hr style="margin: 20px 0;">
        
        <div class="control-group">
            <label for="fontSize">Font Size:</label>
            <select id="fontSize" onchange="updateFontSize()">
                <option value="font-small">Small</option>
                <option value="font-medium" selected>Medium</option>
                <option value="font-large">Large</option>
            </select>
        </div>

        <div class="control-group">
            <label for="borderSize">Border Size:</label>
            <select id="borderSize" onchange="updateTableStyles()">
                <option value="2px" selected>Medium (2px)</option>
                <option value="1px">Thin (1px)</option>
                <option value="3px">Thick (3px)</option>
            </select>
        </div>
    </div>

    <div class="a4-paper font-medium" id="memoArea">
        <header> </header>
        <div class="invoice-info"> </div>
        <table id="memoTable"> </table>
        {% if notes %}
        <div class="notes-section" style="margin-top: 4px; font-size: 110px; color: #92400e;">
    <p><strong>⭐:</strong> {{ notes }}</p>
</div>
        {% endif %}
    </div>

    <div id="capture-container"></div>

<script>
    const toBanglaDigits = (number) => {
        const banglaDigits = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
        return String(number).replace(/\d/g, d => banglaDigits[d]);
    };

    function updateHeaderSpacing() {
        const topMargin = document.getElementById('headerTopMargin').value;
        const bottomMargin = document.getElementById('headerBottomMargin').value;
        document.documentElement.style.setProperty('--header-top-margin', topMargin + 'px');
        document.documentElement.style.setProperty('--header-bottom-margin', bottomMargin + 'px');
        document.getElementById('headerTopMarginValue').textContent = topMargin;
        document.getElementById('headerBottomMarginValue').textContent = bottomMargin;
    }

    function updateFontSize() {
        const selectedSize = document.getElementById('fontSize').value;
        const memoArea = document.getElementById('memoArea');
        memoArea.classList.remove('font-small', 'font-medium', 'font-large');
        memoArea.classList.add(selectedSize);
    }

    function updateTableStyles() {
        const borderSize = document.getElementById('borderSize').value;
        document.documentElement.style.setProperty('--border-width', borderSize);
    }
    
    const sleep = ms => new Promise(res => setTimeout(res, ms));
    function downloadDataUrl(dataUrl, filename) {
        const a = document.createElement('a');
        a.href = dataUrl; a.download = filename;
        document.body.appendChild(a); a.click(); a.remove();
    }

    async function waitForFontLoading() {
        try {
            await document.fonts.load('normal 12px MyCustomFont');
        } catch (e) { console.warn("Font could not be loaded in time.", e); }
    }
    
    async function generateMultiPageMemo() {
        const printButton = document.getElementById('printMemo');
        printButton.disabled = true;
        printButton.textContent = 'মেমো তৈরি হচ্ছে...';

        await waitForFontLoading();

        const originalMemo = document.getElementById('memoArea');
        const captureContainer = document.getElementById('capture-container');
        captureContainer.innerHTML = ''; 

        const header = originalMemo.querySelector('header');
        const invoiceInfo = originalMemo.querySelector('.invoice-info');
        
        // Correctly get memo number and date text
        const memoNumberEl = document.getElementById('memo-number-display');
        const dateEl = document.getElementById('memo-date-display');
        const memoNumberText = memoNumberEl ? memoNumberEl.textContent.trim() : '';
        const dateText = dateEl ? dateEl.textContent.trim() : '';

        const table = originalMemo.querySelector('#memoTable');
        const tableHead = table.querySelector('thead');
        const tableFoot = table.querySelector('tfoot');
        const allRows = Array.from(table.querySelectorAll('tbody tr'));
        const notesSection = originalMemo.querySelector('.notes-section');
        
        const A4_PAGE_HEIGHT = 3508;
        const BOTTOM_MARGIN = 0; 

        const averageRowHeight = allRows.length > 0 ? allRows[0].offsetHeight : 150;

        let rowsLeft = [...allRows];
        let pageNumber = 1;

        while (rowsLeft.length > 0) {
            const newPage = document.createElement('div');
            newPage.className = originalMemo.className;
            captureContainer.appendChild(newPage);
            
            let pageContentHeight = 0;

            if (pageNumber === 1) {
                const headerClone = header.cloneNode(true);
                newPage.appendChild(headerClone);
                const invoiceInfoClone = invoiceInfo.cloneNode(true);
                newPage.appendChild(invoiceInfoClone);
                pageContentHeight += header.offsetHeight + invoiceInfo.offsetHeight;
            } else {
                // Add simplified header for subsequent pages
                const subsequentPageHeader = document.createElement('div');
                subsequentPageHeader.style.textAlign = 'left';
                subsequentPageHeader.style.padding = '0px 0px 0px 0px';
                subsequentPageHeader.style.fontSize = '90px';
                subsequentPageHeader.style.fontWeight = 'bold';
                subsequentPageHeader.style.color = '#7c2d12';
                subsequentPageHeader.innerHTML = `<p>${memoNumberText} | ${dateText} | পাতা: ${toBanglaDigits(pageNumber)}</p>`;
                newPage.appendChild(subsequentPageHeader);
                pageContentHeight += 150; // Estimated height for this header
            }

            const newPageTable = document.createElement('table');
            const tableHeadClone = tableHead.cloneNode(true);
            newPageTable.appendChild(tableHeadClone);
            const newPageTbody = document.createElement('tbody');
            newPageTable.appendChild(newPageTbody);
            newPage.appendChild(newPageTable);
            
            pageContentHeight += tableHead.offsetHeight;

            let availableHeight = A4_PAGE_HEIGHT - pageContentHeight - BOTTOM_MARGIN;
            
            const potentialFooterHeight = tableFoot.offsetHeight + (notesSection ? notesSection.offsetHeight : 0);
            
            while (rowsLeft.length > 0) {
                const rowHeight = rowsLeft[0].offsetHeight > 0 ? rowsLeft[0].offsetHeight : averageRowHeight;
                
                let spaceNeeded = (rowsLeft.length === 1) ? rowHeight + potentialFooterHeight : rowHeight;

                if (availableHeight - spaceNeeded < 0) {
                    break; 
                }
                
                availableHeight -= rowHeight;
                newPageTbody.appendChild(rowsLeft.shift().cloneNode(true));
            }
            
            if (rowsLeft.length === 0) {
                newPageTable.appendChild(tableFoot.cloneNode(true));
                if (notesSection) {
                    newPage.appendChild(notesSection.cloneNode(true));
                }
            }
            pageNumber++;
        }
        
        await sleep(500);

        const pagesToCapture = captureContainer.querySelectorAll('.a4-paper');
        for (let i = 0; i < pagesToCapture.length; i++) {
            printButton.textContent = `পার্ট ${i + 1} ডাউনলোড হচ্ছে...`;
            try {
                const canvas = await html2canvas(pagesToCapture[i], { scale: 1.5, useCORS: true });
                downloadDataUrl(canvas.toDataURL('image/png', 1.0), `memo-part-${i + 1}.png`);
                await sleep(1000);
            } catch (error) {
                alert(`পার্ট ${i + 1} তৈরি করতে সমস্যা হয়েছে।`);
                console.error('Capture error:', error);
                break;
            }
        }

        printButton.disabled = false;
        printButton.textContent = '🖨️ মেমো ডাউনলোড করুন';
        captureContainer.innerHTML = '';
    }

    document.addEventListener('DOMContentLoaded', function() {
        const memoArea = document.getElementById('memoArea');
        memoArea.querySelector('header').innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 0px 0px;">
                <img src="{{ left_logo_url }}" alt="বাম লোগো" class="logo">
                <div style="text-align: center; flex: 1; margin: 0 30px;">
                    <h1>{{ company_name }}</h1> <p>{{ company_owner }}</p> <p>{{ company_address }}</p>
                    <p class="phone-info">ফোন (ডিলার): {{ company_phone }} | প্রেস্টিজ: {{ company_email }} | প্যাসিফিক: {{ company_email2 }}</p>
                </div>
                <img src="{{ right_logo_url }}" alt="ডান লোগো" class="logo">
            </div>`;

        memoArea.querySelector('.invoice-info').innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div> <p><strong>গ্রাহকের নাম:</strong> {{ customer }}</p> <p><strong>ঠিকানা:</strong> {{ address }}</p> </div>
                <div style="text-align: right;"> 
                    <p id="memo-number-display"><strong>মেমো নম্বর:</strong> {{ invoice_no|to_bangla_digits }}</p> 
                    <p id="memo-date-display"><strong>তারিখ:</strong> {{ date|to_bangla_digits }}</p> 
                </div>
            </div>`;

        const memoTable = memoArea.querySelector('#memoTable');
        memoTable.innerHTML = `
            <thead>
                <tr>
                    <th class="column-product-header" style="width: 67%;">পণ্যের নাম</th> 
                    <th class="column-quantity-header" style="width: 7%;">পরিমাণ</th>
                    <th class="column-price-header" style="width: 14%;">মূল্য</th> 
                    <th class="column-total-header" style="width: 12%;">মোট</th>
                </tr>
            </thead>
            <tbody>
                {% for item in items %}
                <tr>
                    <td class="column-product-cell">{{ item.item }}</td> 
                    <td class="column-quantity-cell">{{ item.price|round(2)|to_bangla_digits }}</td>
                    <td class="column-price-cell">{{ item.qty|to_bangla_digits }} {{ item.unit }}</td> 
                    <td class="column-total-cell">{{ item.total|round(2)|to_bangla_digits }}</td>
                </tr>
                {% endfor %}
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="3" style="text-align: right;"><strong>{% if discount_percent > 0 or previous_due > 0 %}মোট মাল{% else %}সর্বমোট{% endif %}</strong></td>
                    <td class="column-total-cell"><strong>{{ total|round(2)|to_bangla_digits }}</strong></td>
                </tr>
        
                {% if discount_percent > 0 %}
                <tr>
                    <td colspan="3" style="text-align: right;"><strong>ডিসকাউন্ট ({{ discount_percent|round(2)|to_bangla_digits }}%)</strong></td>
                    <td class="column-total-cell"><strong>- {{ discount_amount|round(2)|to_bangla_digits }}</strong></td>
                </tr>
                <tr>
                    <td colspan="3" style="text-align: right;"><strong>ডিসকাউন্ট পর</strong></td>
                    <td class="column-total-cell"><strong>{{ (total - discount_amount)|round(2)|to_bangla_digits }}</strong></td>
                </tr>
                {% endif %}
        
                {% if previous_due > 0 %}
                <tr>
                    <td colspan="3" style="text-align: right;"><strong>আগের বাকি</strong></td>
                    <td class="column-total-cell"><strong>{{ previous_due|round(2)|to_bangla_digits }}</strong></td>
                </tr>
                {% endif %}
        
                {% if discount_percent > 0 or previous_due > 0 %}
                <tr>
                    <td colspan="3" style="text-align: right;"><strong>সর্বমোট</strong></td>
                    <td class="column-total-cell"><strong>{{ grand_total|round(2)|to_bangla_digits }}</strong></td>
                </tr>
                {% endif %}
            </tfoot>
            `;
        
        updateHeaderSpacing();
        updateTableStyles();
        updateFontSize();
        
        document.getElementById("printMemo").addEventListener("click", generateMultiPageMemo);
    });
</script>
</body>
</html>
"""

@app.route('/')
def index():
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    local_left_logo = url_for('static', filename='left_logo.png', _external=True)
    local_right_logo = url_for('static', filename='right_logo.png', _external=True)

    return render_template_string(form_template,
                                 company_name=company_name,
                                 company_owner=company_owner,
                                 company_address=company_address,
                                 company_phone=company_phone,
                                 company_email=company_email,
                                 company_email2=company_email2,
                                 left_logo_url=local_left_logo,
                                 right_logo_url=local_right_logo,
                                 products=products,
                                 customers=customers,
                                 customer_addresses=customer_addresses,
                                 addresses=addresses,
                                 today=today,
                                 invoice_no=0)


@app.route('/generate', methods=['POST'])
def generate():
    try:
        customer = request.form['customer']
        address = request.form['address']
        date_from_form = request.form['date']
        items_json = request.form['items']
        invoice_no = request.form['invoice_no']
        discount_percent = float(request.form.get('discount', 0) or 0)
        notes = request.form.get('notes', '')
        previous_due = float(request.form.get('previous_due', 0) or 0)

        if not customer or not items_json:
            return "Error: Customer name and items are required", 400

        date_obj = datetime.datetime.strptime(date_from_form, '%Y-%m-%d').date()
        formatted_date = date_obj.strftime('%d-%m-%Y')

        items = json.loads(items_json) if items_json else []
        total = sum(item['total'] for item in items)
        
        discount_amount = (total * discount_percent) / 100
        total_after_discount = total - discount_amount
        grand_total = total_after_discount + previous_due

        local_left_logo = url_for('static', filename='left_logo.png', _external=True)
        local_right_logo = url_for('static', filename='right_logo.png', _external=True)

        return render_template_string(memo_template,
                                     company_name=company_name,
                                     company_owner=company_owner,
                                     company_address=company_address,
                                     company_phone=company_phone,
                                     company_email=company_email,
                                     company_email2=company_email2,
                                     left_logo_url=local_left_logo,
                                     right_logo_url=local_right_logo,
                                     customer=customer,
                                     address=address,
                                     date=formatted_date,
                                     items=items,
                                     total=total,
                                     invoice_no=invoice_no,
                                     discount_percent=discount_percent,
                                     discount_amount=discount_amount,
                                     grand_total=grand_total,
                                     previous_due=previous_due,
                                     notes=notes)
    except Exception as e:
        return f"Error generating memo: {str(e)}", 500

# ... (rest of the code remains the same for collage functionality)
# COLLAGE BLUEPRINT - FIXED VERSION
marge_bp = Blueprint("marge", __name__, url_prefix="/Marge")

A4_WIDTH, A4_HEIGHT = 2480, 3508
ROWS, COLS = 2, 2
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def make_a4_collage(image_paths, output_path):
    collage = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    gap_x = 64  # horizontal gap (middle vertical line)
    gap_y = 66  # vertical gap (middle horizontal line)

    # Each slot shrinks by half the gap on each touching side
    slot_width = (A4_WIDTH - gap_x) // COLS
    slot_height = (A4_HEIGHT - gap_y) // ROWS

    for idx in range(ROWS * COLS):
        row, col = divmod(idx, COLS)

        # Base positions
        x = col * slot_width
        y = row * slot_height

        # Shift right column by half horizontal gap
        if col == 1:
            x += gap_x

        # Shift bottom row by half vertical gap
        if row == 1:
            y += gap_y

        if idx < len(image_paths):
            img = Image.open(image_paths[idx])
            img.thumbnail((slot_width, slot_height), Image.LANCZOS)

            offset_x = x + (slot_width - img.width) // 2
            offset_y = y + (slot_height - img.height) // 2
            collage.paste(img, (offset_x, offset_y))

    collage.save(output_path, "JPEG", quality=100)

# HTML template for the collage page
collage_template = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ফটো কলাজ জেনারেটর</title>
    <style>
        body { 
            font-family: 'Arial', sans-serif; 
            background: #fef7ed; 
            margin: 0; 
            padding: 20px; 
        }
        .container { 
            max-width: 600px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            border: 2px solid #fdba74;
        }
        h1 { 
            color: #ea580c; 
            text-align: center; 
            margin-bottom: 30px; 
        }
        .upload-form { 
            border: 2px dashed #fdba74; 
            padding: 30px; 
            text-align: center; 
            border-radius: 8px; 
            margin-bottom: 20px; 
            background: #fffbeb;
        }
        .file-input { 
            margin: 15px 0; 
        }
        .generate-btn { 
            background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
            color: white; 
            border: none; 
            padding: 12px 30px; 
            border-radius: 6px; 
            cursor: pointer; 
            font-size: 16px; 
            width: 100%; 
        }
        .generate-btn:hover { 
            background: linear-gradient(135deg, #c2410c 0%, #9a3412 100%);
        }
        .note { 
            background: #fef3c7; 
            padding: 15px; 
            border-radius: 6px; 
            margin-top: 20px; 
            font-size: 14px; 
            color: #92400e; 
            border: 1px solid #f59e0b;
        }
        .back-link { 
            display: block; 
            text-align: center; 
            margin-top: 20px; 
            color: #ea580c; 
            text-decoration: none; 
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📸 ফটো কলাজ জেনারেটর</h1>
        
        <form method="post" enctype="multipart/form-data" class="upload-form">
            <div class="file-input">
                <strong style="color: #7c2d12;">৪টি ছবি নির্বাচন করুন (সর্বোচ্চ ৪টি):</strong><br>
                <input type="file" name="photos" multiple accept="image/*" required>
            </div>
            <button type="submit" class="generate-btn">📥 কলাজ জেনারেট করুন</button>
        </form>
        
        <div class="note">
            <strong>নির্দেশনা:</strong><br>
            • সর্বোচ্চ ৪টি ছবি আপলোড করুন<br>
            • ছবিগুলো JPG, PNG, JPEG ফরম্যাটে হতে হবে<br>
            • কলাজটি A4 সাইজে তৈরি হবে<br>
            • আপলোডেট কলাজ ডাউনলোড হবে স্বয়ংক্রিয়ভাবে
        </div>
        
        <a href="{{ url_for('index') }}" class="back-link">← মেমো জেনারেটরে ফিরে যান</a>
    </div>
</body>
</html>
"""

@marge_bp.route("/", methods=["GET", "POST"])
def collage_index():
    if request.method == "POST":
        if 'photos' not in request.files:
            return "কোন ফাইল নির্বাচন করা হয়নি", 400
        
        uploaded_files = request.files.getlist("photos")
        
        if not uploaded_files or uploaded_files[0].filename == '':
            return "কোন ফাইল নির্বাচন করা হয়নি", 400
        
        paths = []
        
        try:
            for file in uploaded_files[:4]:
                if file and file.filename:
                    if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                        return "শুধুমাত্র JPG, JPEG, PNG ফাইল অনুমোদিত", 400
                    
                    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    paths.append(filepath)
            
            if not paths:
                return "কোন বৈধ ছবি পাওয়া যায়নি", 400
            
            output_filename = str(uuid.uuid4()) + ".jpg"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            make_a4_collage(paths, output_path)
            
            for path in paths:
                if os.path.exists(path):
                    os.remove(path)
            
            return send_file(output_path, as_attachment=True, download_name=f"collage_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
            
        except Exception as e:
            for path in paths:
                if os.path.exists(path):
                    os.remove(path)
            return f"ত্রুটি ঘটেছে: {str(e)}", 500
    
    return render_template_string(collage_template)

# Register the blueprint
app.register_blueprint(marge_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3737, debug=True, use_reloader=False)
