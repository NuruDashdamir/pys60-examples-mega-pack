


<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
 <link rel="icon" type="image/vnd.microsoft.icon" href="http://www.gstatic.com/codesite/ph/images/phosting.ico">
 
 <script type="text/javascript">
 
 
 
 var codesite_token = null;
 
 
 var logged_in_user_email = null;
 
 
 var relative_base_url = "";
 
 </script>
 
 
 <title>canvaslistbox.py - 
 wordmobi -
 
 Project Hosting on Google Code</title>
 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" >
 
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/7642550995449508181/css/ph_core.css">
 
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/7642550995449508181/css/ph_detail.css" >
 
 
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/7642550995449508181/css/d_sb_20080522.css" >
 
 
 
<!--[if IE]>
 <link type="text/css" rel="stylesheet" href="http://www.gstatic.com/codesite/ph/7642550995449508181/css/d_ie.css" >
<![endif]-->
 <style type="text/css">
 .menuIcon.off { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 -42px }
 .menuIcon.on { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 -28px }
 .menuIcon.down { background: no-repeat url(http://www.gstatic.com/codesite/ph/images/dropdown_sprite.gif) 0 0; }
 </style>
</head>
<body class="t4">
 <script type="text/javascript">
 var _gaq = _gaq || [];
 _gaq.push(
 ['siteTracker._setAccount', 'UA-18071-1'],
 ['siteTracker._trackPageview']);
 
 _gaq.push(
 ['projectTracker._setAccount', 'UA-2194725-6'],
 ['projectTracker._trackPageview']);
 
 (function() {
 var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
 ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
 (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(ga);
 })();
 </script>
 <div id="gaia">
 
 <span>
 
 <a href="#" id="projects-dropdown" onclick="return false;"><u>My favorites</u> <small>&#9660;</small></a>
 | <a href="https://www.google.com/accounts/ServiceLogin?service=code&amp;ltmpl=phosting&amp;continue=http%3A%2F%2Fcode.google.com%2Fp%2Fwordmobi%2Fsource%2Fbrowse%2Ftrunk%2Fcanvaslistbox%2Fcanvaslistbox.py&amp;followup=http%3A%2F%2Fcode.google.com%2Fp%2Fwordmobi%2Fsource%2Fbrowse%2Ftrunk%2Fcanvaslistbox%2Fcanvaslistbox.py" onclick="_CS_click('/gb/ph/signin');"><u>Sign in</u></a>
 
 </span>

 </div>
 <div class="gbh" style="left: 0pt;"></div>
 <div class="gbh" style="right: 0pt;"></div>
 
 
 <div style="height: 1px"></div>
<!--[if IE 6]>
<div style="text-align:center;">
Support browsers that contribute to open source, try <a href="http://www.firefox.com">Firefox</a> or <a href="http://www.google.com/chrome">Google Chrome</a>.
</div>
<![endif]-->




 <table style="padding:0px; margin: 20px 0px 0px 0px; width:100%" cellpadding="0" cellspacing="0">
 <tr style="height: 58px;">
 
 <td style="width: 55px; text-align:center;">
 <a href="/p/wordmobi/">
 
 
 <img src="/p/wordmobi/logo?cct=1238260372" alt="Logo">
 
 </a>
 </td>
 
 <td style="padding-left: 0.5em">
 
 <div id="pname" style="margin: 0px 0px -3px 0px">
 <a href="/p/wordmobi/" style="text-decoration:none; color:#000">wordmobi</a>
 
 </div>
 <div id="psum">
 <i><a id="project_summary_link" href="/p/wordmobi/" style="text-decoration:none; color:#000">Keep Blogging™</a></i>
 </div>
 
 </td>
 <td style="white-space:nowrap;text-align:right">
 
 <form action="/hosting/search">
 <input size="30" name="q" value="">
 <input type="submit" name="projectsearch" value="Search projects" >
 </form>
 
 </tr>
 </table>


 
<table id="mt" cellspacing="0" cellpadding="0" width="100%" border="0">
 <tr>
 <th onclick="if (!cancelBubble) _go('/p/wordmobi/');">
 <div class="tab inactive">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <a onclick="cancelBubble=true;" href="/p/wordmobi/">Project&nbsp;Home</a>
 </div>
 </div>
 </th><td>&nbsp;&nbsp;</td>
 
 
 
 
 <th onclick="if (!cancelBubble) _go('/p/wordmobi/downloads/list');">
 <div class="tab inactive">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <a onclick="cancelBubble=true;" href="/p/wordmobi/downloads/list">Downloads</a>
 </div>
 </div>
 </th><td>&nbsp;&nbsp;</td>
 
 
 
 
 
 <th onclick="if (!cancelBubble) _go('/p/wordmobi/w/list');">
 <div class="tab inactive">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <a onclick="cancelBubble=true;" href="/p/wordmobi/w/list">Wiki</a>
 </div>
 </div>
 </th><td>&nbsp;&nbsp;</td>
 
 
 
 
 
 <th onclick="if (!cancelBubble) _go('/p/wordmobi/issues/list');">
 <div class="tab inactive">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <a onclick="cancelBubble=true;" href="/p/wordmobi/issues/list">Issues</a>
 </div>
 </div>
 </th><td>&nbsp;&nbsp;</td>
 
 
 
 
 
 <th onclick="if (!cancelBubble) _go('/p/wordmobi/source/checkout');">
 <div class="tab active">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <a onclick="cancelBubble=true;" href="/p/wordmobi/source/checkout">Source</a>
 </div>
 </div>
 </th><td>&nbsp;&nbsp;</td>
 
 
 <td width="100%">&nbsp;</td>
 </tr>
</table>
<table cellspacing="0" cellpadding="0" width="100%" align="center" border="0" class="st">
 <tr>
 
 
 
 
 
 
 <td>
 <div class="st2">
 <div class="isf">
 
 
 
 <span class="inst1"><a href="/p/wordmobi/source/checkout">Checkout</a></span> |
 <span class="inst2"><a href="/p/wordmobi/source/browse/">Browse</a></span> |
 <span class="inst3"><a href="/p/wordmobi/source/list">Changes</a></span> |
 
 <form action="http://www.google.com/codesearch" method="get" style="display:inline"
 onsubmit="document.getElementById('codesearchq').value = document.getElementById('origq').value + ' package:http://wordmobi\\.googlecode\\.com'">
 <input type="hidden" name="q" id="codesearchq" value="">
 <input maxlength="2048" size="38" id="origq" name="origq" value="" title="Google Code Search" style="font-size:92%">&nbsp;<input type="submit" value="Search Trunk" name="btnG" style="font-size:92%">
 
 
 
 </form>
 </div>
</div>

 </td>
 
 
 
 <td height="4" align="right" valign="top" class="bevel-right">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 </td>
 </tr>
</table>
<script type="text/javascript">
 var cancelBubble = false;
 function _go(url) { document.location = url; }
</script>


<div id="maincol"
 
>

 
<!-- IE -->




<div class="expand">


<style type="text/css">
 #file_flipper { display: inline; float: right; white-space: nowrap; }
 #file_flipper.hidden { display: none; }
 #file_flipper .pagelink { color: #0000CC; text-decoration: underline; }
 #file_flipper #visiblefiles { padding-left: 0.5em; padding-right: 0.5em; }
</style>
<div id="nav_and_rev" class="heading">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner" id="bub">
 <div class="bub-top">
 <div class="pagination" style="margin-left: 2em">
 <table cellpadding="0" cellspacing="0" class="flipper">
 <tbody>
 <tr>
 
 <td><b>r704</b></td>
 
 </tr>
 </tbody>
 </table>
 </div>
 
 <div class="" style="vertical-align: top">
 <div class="src_crumbs src_nav">
 <strong class="src_nav">Source path:&nbsp;</strong>
 <span id="crumb_root">
 
 <a href="/p/wordmobi/source/browse/">svn</a>/&nbsp;</span>
 <span id="crumb_links" class="ifClosed"><a href="/p/wordmobi/source/browse/trunk/">trunk</a><span class="sp">/&nbsp;</span><a href="/p/wordmobi/source/browse/trunk/canvaslistbox/">canvaslistbox</a><span class="sp">/&nbsp;</span>canvaslistbox.py</span>
 
 
 </div>
 
 </div>
 <div style="clear:both"></div>
 </div>
 </div>
</div>

<style type="text/css">
 
  tr.inline_comment {
 background: #fff;
 vertical-align: top;
 }
 div.draft, div.published {
 padding: .3em;
 border: 1px solid #999; 
 margin-bottom: .1em;
 font-family: arial, sans-serif;
 max-width: 60em;
 }
 div.draft {
 background: #ffa;
 } 
 div.published {
 background: #e5ecf9;
 }
 div.published .body, div.draft .body {
 padding: .5em .1em .1em .1em;
 max-width: 60em;
 white-space: pre-wrap;
 white-space: -moz-pre-wrap;
 white-space: -pre-wrap;
 white-space: -o-pre-wrap;
 word-wrap: break-word;
 }
 div.draft .actions {
 margin-left: 1em;
 font-size: 90%;
 }
 div.draft form {
 padding: .5em .5em .5em 0;
 }
 div.draft textarea, div.published textarea {
 width: 95%;
 height: 10em;
 font-family: arial, sans-serif;
 margin-bottom: .5em;
 }


 
 .nocursor, .nocursor td, .cursor_hidden, .cursor_hidden td {
 background-color: white;
 height: 2px;
 }
 .cursor, .cursor td {
 background-color: darkblue;
 height: 2px;
 display: '';
 }

</style>
<div class="fc">
 
 
 
<style type="text/css">
.undermouse span { 
 background-image: url(http://www.gstatic.com/codesite/ph/images/comments.gif); }
</style>
<table class="opened" id="review_comment_area" 
><tr>
<td id="nums">
<pre><table width="100%"><tr class="nocursor"><td></td></tr></table></pre>

<pre><table width="100%" id="nums_table_0"><tr id="gr_svn496_1"

><td id="1"><a href="#1">1</a></td></tr
><tr id="gr_svn496_2"

><td id="2"><a href="#2">2</a></td></tr
><tr id="gr_svn496_3"

><td id="3"><a href="#3">3</a></td></tr
><tr id="gr_svn496_4"

><td id="4"><a href="#4">4</a></td></tr
><tr id="gr_svn496_5"

><td id="5"><a href="#5">5</a></td></tr
><tr id="gr_svn496_6"

><td id="6"><a href="#6">6</a></td></tr
><tr id="gr_svn496_7"

><td id="7"><a href="#7">7</a></td></tr
><tr id="gr_svn496_8"

><td id="8"><a href="#8">8</a></td></tr
><tr id="gr_svn496_9"

><td id="9"><a href="#9">9</a></td></tr
><tr id="gr_svn496_10"

><td id="10"><a href="#10">10</a></td></tr
><tr id="gr_svn496_11"

><td id="11"><a href="#11">11</a></td></tr
><tr id="gr_svn496_12"

><td id="12"><a href="#12">12</a></td></tr
><tr id="gr_svn496_13"

><td id="13"><a href="#13">13</a></td></tr
><tr id="gr_svn496_14"

><td id="14"><a href="#14">14</a></td></tr
><tr id="gr_svn496_15"

><td id="15"><a href="#15">15</a></td></tr
><tr id="gr_svn496_16"

><td id="16"><a href="#16">16</a></td></tr
><tr id="gr_svn496_17"

><td id="17"><a href="#17">17</a></td></tr
><tr id="gr_svn496_18"

><td id="18"><a href="#18">18</a></td></tr
><tr id="gr_svn496_19"

><td id="19"><a href="#19">19</a></td></tr
><tr id="gr_svn496_20"

><td id="20"><a href="#20">20</a></td></tr
><tr id="gr_svn496_21"

><td id="21"><a href="#21">21</a></td></tr
><tr id="gr_svn496_22"

><td id="22"><a href="#22">22</a></td></tr
><tr id="gr_svn496_23"

><td id="23"><a href="#23">23</a></td></tr
><tr id="gr_svn496_24"

><td id="24"><a href="#24">24</a></td></tr
><tr id="gr_svn496_25"

><td id="25"><a href="#25">25</a></td></tr
><tr id="gr_svn496_26"

><td id="26"><a href="#26">26</a></td></tr
><tr id="gr_svn496_27"

><td id="27"><a href="#27">27</a></td></tr
><tr id="gr_svn496_28"

><td id="28"><a href="#28">28</a></td></tr
><tr id="gr_svn496_29"

><td id="29"><a href="#29">29</a></td></tr
><tr id="gr_svn496_30"

><td id="30"><a href="#30">30</a></td></tr
><tr id="gr_svn496_31"

><td id="31"><a href="#31">31</a></td></tr
><tr id="gr_svn496_32"

><td id="32"><a href="#32">32</a></td></tr
><tr id="gr_svn496_33"

><td id="33"><a href="#33">33</a></td></tr
><tr id="gr_svn496_34"

><td id="34"><a href="#34">34</a></td></tr
><tr id="gr_svn496_35"

><td id="35"><a href="#35">35</a></td></tr
><tr id="gr_svn496_36"

><td id="36"><a href="#36">36</a></td></tr
><tr id="gr_svn496_37"

><td id="37"><a href="#37">37</a></td></tr
><tr id="gr_svn496_38"

><td id="38"><a href="#38">38</a></td></tr
><tr id="gr_svn496_39"

><td id="39"><a href="#39">39</a></td></tr
><tr id="gr_svn496_40"

><td id="40"><a href="#40">40</a></td></tr
><tr id="gr_svn496_41"

><td id="41"><a href="#41">41</a></td></tr
><tr id="gr_svn496_42"

><td id="42"><a href="#42">42</a></td></tr
><tr id="gr_svn496_43"

><td id="43"><a href="#43">43</a></td></tr
><tr id="gr_svn496_44"

><td id="44"><a href="#44">44</a></td></tr
><tr id="gr_svn496_45"

><td id="45"><a href="#45">45</a></td></tr
><tr id="gr_svn496_46"

><td id="46"><a href="#46">46</a></td></tr
><tr id="gr_svn496_47"

><td id="47"><a href="#47">47</a></td></tr
><tr id="gr_svn496_48"

><td id="48"><a href="#48">48</a></td></tr
><tr id="gr_svn496_49"

><td id="49"><a href="#49">49</a></td></tr
><tr id="gr_svn496_50"

><td id="50"><a href="#50">50</a></td></tr
><tr id="gr_svn496_51"

><td id="51"><a href="#51">51</a></td></tr
><tr id="gr_svn496_52"

><td id="52"><a href="#52">52</a></td></tr
><tr id="gr_svn496_53"

><td id="53"><a href="#53">53</a></td></tr
><tr id="gr_svn496_54"

><td id="54"><a href="#54">54</a></td></tr
><tr id="gr_svn496_55"

><td id="55"><a href="#55">55</a></td></tr
><tr id="gr_svn496_56"

><td id="56"><a href="#56">56</a></td></tr
><tr id="gr_svn496_57"

><td id="57"><a href="#57">57</a></td></tr
><tr id="gr_svn496_58"

><td id="58"><a href="#58">58</a></td></tr
><tr id="gr_svn496_59"

><td id="59"><a href="#59">59</a></td></tr
><tr id="gr_svn496_60"

><td id="60"><a href="#60">60</a></td></tr
><tr id="gr_svn496_61"

><td id="61"><a href="#61">61</a></td></tr
><tr id="gr_svn496_62"

><td id="62"><a href="#62">62</a></td></tr
><tr id="gr_svn496_63"

><td id="63"><a href="#63">63</a></td></tr
><tr id="gr_svn496_64"

><td id="64"><a href="#64">64</a></td></tr
><tr id="gr_svn496_65"

><td id="65"><a href="#65">65</a></td></tr
><tr id="gr_svn496_66"

><td id="66"><a href="#66">66</a></td></tr
><tr id="gr_svn496_67"

><td id="67"><a href="#67">67</a></td></tr
><tr id="gr_svn496_68"

><td id="68"><a href="#68">68</a></td></tr
><tr id="gr_svn496_69"

><td id="69"><a href="#69">69</a></td></tr
><tr id="gr_svn496_70"

><td id="70"><a href="#70">70</a></td></tr
><tr id="gr_svn496_71"

><td id="71"><a href="#71">71</a></td></tr
><tr id="gr_svn496_72"

><td id="72"><a href="#72">72</a></td></tr
><tr id="gr_svn496_73"

><td id="73"><a href="#73">73</a></td></tr
><tr id="gr_svn496_74"

><td id="74"><a href="#74">74</a></td></tr
><tr id="gr_svn496_75"

><td id="75"><a href="#75">75</a></td></tr
><tr id="gr_svn496_76"

><td id="76"><a href="#76">76</a></td></tr
><tr id="gr_svn496_77"

><td id="77"><a href="#77">77</a></td></tr
><tr id="gr_svn496_78"

><td id="78"><a href="#78">78</a></td></tr
><tr id="gr_svn496_79"

><td id="79"><a href="#79">79</a></td></tr
><tr id="gr_svn496_80"

><td id="80"><a href="#80">80</a></td></tr
><tr id="gr_svn496_81"

><td id="81"><a href="#81">81</a></td></tr
><tr id="gr_svn496_82"

><td id="82"><a href="#82">82</a></td></tr
><tr id="gr_svn496_83"

><td id="83"><a href="#83">83</a></td></tr
><tr id="gr_svn496_84"

><td id="84"><a href="#84">84</a></td></tr
><tr id="gr_svn496_85"

><td id="85"><a href="#85">85</a></td></tr
><tr id="gr_svn496_86"

><td id="86"><a href="#86">86</a></td></tr
><tr id="gr_svn496_87"

><td id="87"><a href="#87">87</a></td></tr
><tr id="gr_svn496_88"

><td id="88"><a href="#88">88</a></td></tr
><tr id="gr_svn496_89"

><td id="89"><a href="#89">89</a></td></tr
><tr id="gr_svn496_90"

><td id="90"><a href="#90">90</a></td></tr
><tr id="gr_svn496_91"

><td id="91"><a href="#91">91</a></td></tr
><tr id="gr_svn496_92"

><td id="92"><a href="#92">92</a></td></tr
><tr id="gr_svn496_93"

><td id="93"><a href="#93">93</a></td></tr
><tr id="gr_svn496_94"

><td id="94"><a href="#94">94</a></td></tr
><tr id="gr_svn496_95"

><td id="95"><a href="#95">95</a></td></tr
><tr id="gr_svn496_96"

><td id="96"><a href="#96">96</a></td></tr
><tr id="gr_svn496_97"

><td id="97"><a href="#97">97</a></td></tr
><tr id="gr_svn496_98"

><td id="98"><a href="#98">98</a></td></tr
><tr id="gr_svn496_99"

><td id="99"><a href="#99">99</a></td></tr
><tr id="gr_svn496_100"

><td id="100"><a href="#100">100</a></td></tr
><tr id="gr_svn496_101"

><td id="101"><a href="#101">101</a></td></tr
><tr id="gr_svn496_102"

><td id="102"><a href="#102">102</a></td></tr
><tr id="gr_svn496_103"

><td id="103"><a href="#103">103</a></td></tr
><tr id="gr_svn496_104"

><td id="104"><a href="#104">104</a></td></tr
><tr id="gr_svn496_105"

><td id="105"><a href="#105">105</a></td></tr
><tr id="gr_svn496_106"

><td id="106"><a href="#106">106</a></td></tr
><tr id="gr_svn496_107"

><td id="107"><a href="#107">107</a></td></tr
><tr id="gr_svn496_108"

><td id="108"><a href="#108">108</a></td></tr
><tr id="gr_svn496_109"

><td id="109"><a href="#109">109</a></td></tr
><tr id="gr_svn496_110"

><td id="110"><a href="#110">110</a></td></tr
><tr id="gr_svn496_111"

><td id="111"><a href="#111">111</a></td></tr
><tr id="gr_svn496_112"

><td id="112"><a href="#112">112</a></td></tr
><tr id="gr_svn496_113"

><td id="113"><a href="#113">113</a></td></tr
><tr id="gr_svn496_114"

><td id="114"><a href="#114">114</a></td></tr
><tr id="gr_svn496_115"

><td id="115"><a href="#115">115</a></td></tr
><tr id="gr_svn496_116"

><td id="116"><a href="#116">116</a></td></tr
><tr id="gr_svn496_117"

><td id="117"><a href="#117">117</a></td></tr
><tr id="gr_svn496_118"

><td id="118"><a href="#118">118</a></td></tr
><tr id="gr_svn496_119"

><td id="119"><a href="#119">119</a></td></tr
><tr id="gr_svn496_120"

><td id="120"><a href="#120">120</a></td></tr
><tr id="gr_svn496_121"

><td id="121"><a href="#121">121</a></td></tr
><tr id="gr_svn496_122"

><td id="122"><a href="#122">122</a></td></tr
><tr id="gr_svn496_123"

><td id="123"><a href="#123">123</a></td></tr
><tr id="gr_svn496_124"

><td id="124"><a href="#124">124</a></td></tr
><tr id="gr_svn496_125"

><td id="125"><a href="#125">125</a></td></tr
><tr id="gr_svn496_126"

><td id="126"><a href="#126">126</a></td></tr
><tr id="gr_svn496_127"

><td id="127"><a href="#127">127</a></td></tr
><tr id="gr_svn496_128"

><td id="128"><a href="#128">128</a></td></tr
><tr id="gr_svn496_129"

><td id="129"><a href="#129">129</a></td></tr
><tr id="gr_svn496_130"

><td id="130"><a href="#130">130</a></td></tr
><tr id="gr_svn496_131"

><td id="131"><a href="#131">131</a></td></tr
><tr id="gr_svn496_132"

><td id="132"><a href="#132">132</a></td></tr
><tr id="gr_svn496_133"

><td id="133"><a href="#133">133</a></td></tr
><tr id="gr_svn496_134"

><td id="134"><a href="#134">134</a></td></tr
><tr id="gr_svn496_135"

><td id="135"><a href="#135">135</a></td></tr
><tr id="gr_svn496_136"

><td id="136"><a href="#136">136</a></td></tr
><tr id="gr_svn496_137"

><td id="137"><a href="#137">137</a></td></tr
><tr id="gr_svn496_138"

><td id="138"><a href="#138">138</a></td></tr
><tr id="gr_svn496_139"

><td id="139"><a href="#139">139</a></td></tr
><tr id="gr_svn496_140"

><td id="140"><a href="#140">140</a></td></tr
><tr id="gr_svn496_141"

><td id="141"><a href="#141">141</a></td></tr
><tr id="gr_svn496_142"

><td id="142"><a href="#142">142</a></td></tr
><tr id="gr_svn496_143"

><td id="143"><a href="#143">143</a></td></tr
><tr id="gr_svn496_144"

><td id="144"><a href="#144">144</a></td></tr
><tr id="gr_svn496_145"

><td id="145"><a href="#145">145</a></td></tr
><tr id="gr_svn496_146"

><td id="146"><a href="#146">146</a></td></tr
><tr id="gr_svn496_147"

><td id="147"><a href="#147">147</a></td></tr
><tr id="gr_svn496_148"

><td id="148"><a href="#148">148</a></td></tr
><tr id="gr_svn496_149"

><td id="149"><a href="#149">149</a></td></tr
><tr id="gr_svn496_150"

><td id="150"><a href="#150">150</a></td></tr
><tr id="gr_svn496_151"

><td id="151"><a href="#151">151</a></td></tr
><tr id="gr_svn496_152"

><td id="152"><a href="#152">152</a></td></tr
><tr id="gr_svn496_153"

><td id="153"><a href="#153">153</a></td></tr
><tr id="gr_svn496_154"

><td id="154"><a href="#154">154</a></td></tr
><tr id="gr_svn496_155"

><td id="155"><a href="#155">155</a></td></tr
><tr id="gr_svn496_156"

><td id="156"><a href="#156">156</a></td></tr
><tr id="gr_svn496_157"

><td id="157"><a href="#157">157</a></td></tr
><tr id="gr_svn496_158"

><td id="158"><a href="#158">158</a></td></tr
><tr id="gr_svn496_159"

><td id="159"><a href="#159">159</a></td></tr
><tr id="gr_svn496_160"

><td id="160"><a href="#160">160</a></td></tr
><tr id="gr_svn496_161"

><td id="161"><a href="#161">161</a></td></tr
><tr id="gr_svn496_162"

><td id="162"><a href="#162">162</a></td></tr
><tr id="gr_svn496_163"

><td id="163"><a href="#163">163</a></td></tr
><tr id="gr_svn496_164"

><td id="164"><a href="#164">164</a></td></tr
><tr id="gr_svn496_165"

><td id="165"><a href="#165">165</a></td></tr
><tr id="gr_svn496_166"

><td id="166"><a href="#166">166</a></td></tr
><tr id="gr_svn496_167"

><td id="167"><a href="#167">167</a></td></tr
><tr id="gr_svn496_168"

><td id="168"><a href="#168">168</a></td></tr
><tr id="gr_svn496_169"

><td id="169"><a href="#169">169</a></td></tr
><tr id="gr_svn496_170"

><td id="170"><a href="#170">170</a></td></tr
><tr id="gr_svn496_171"

><td id="171"><a href="#171">171</a></td></tr
><tr id="gr_svn496_172"

><td id="172"><a href="#172">172</a></td></tr
><tr id="gr_svn496_173"

><td id="173"><a href="#173">173</a></td></tr
><tr id="gr_svn496_174"

><td id="174"><a href="#174">174</a></td></tr
><tr id="gr_svn496_175"

><td id="175"><a href="#175">175</a></td></tr
><tr id="gr_svn496_176"

><td id="176"><a href="#176">176</a></td></tr
><tr id="gr_svn496_177"

><td id="177"><a href="#177">177</a></td></tr
><tr id="gr_svn496_178"

><td id="178"><a href="#178">178</a></td></tr
><tr id="gr_svn496_179"

><td id="179"><a href="#179">179</a></td></tr
><tr id="gr_svn496_180"

><td id="180"><a href="#180">180</a></td></tr
><tr id="gr_svn496_181"

><td id="181"><a href="#181">181</a></td></tr
><tr id="gr_svn496_182"

><td id="182"><a href="#182">182</a></td></tr
><tr id="gr_svn496_183"

><td id="183"><a href="#183">183</a></td></tr
><tr id="gr_svn496_184"

><td id="184"><a href="#184">184</a></td></tr
><tr id="gr_svn496_185"

><td id="185"><a href="#185">185</a></td></tr
><tr id="gr_svn496_186"

><td id="186"><a href="#186">186</a></td></tr
><tr id="gr_svn496_187"

><td id="187"><a href="#187">187</a></td></tr
><tr id="gr_svn496_188"

><td id="188"><a href="#188">188</a></td></tr
><tr id="gr_svn496_189"

><td id="189"><a href="#189">189</a></td></tr
><tr id="gr_svn496_190"

><td id="190"><a href="#190">190</a></td></tr
><tr id="gr_svn496_191"

><td id="191"><a href="#191">191</a></td></tr
><tr id="gr_svn496_192"

><td id="192"><a href="#192">192</a></td></tr
><tr id="gr_svn496_193"

><td id="193"><a href="#193">193</a></td></tr
><tr id="gr_svn496_194"

><td id="194"><a href="#194">194</a></td></tr
><tr id="gr_svn496_195"

><td id="195"><a href="#195">195</a></td></tr
><tr id="gr_svn496_196"

><td id="196"><a href="#196">196</a></td></tr
><tr id="gr_svn496_197"

><td id="197"><a href="#197">197</a></td></tr
><tr id="gr_svn496_198"

><td id="198"><a href="#198">198</a></td></tr
><tr id="gr_svn496_199"

><td id="199"><a href="#199">199</a></td></tr
><tr id="gr_svn496_200"

><td id="200"><a href="#200">200</a></td></tr
><tr id="gr_svn496_201"

><td id="201"><a href="#201">201</a></td></tr
><tr id="gr_svn496_202"

><td id="202"><a href="#202">202</a></td></tr
><tr id="gr_svn496_203"

><td id="203"><a href="#203">203</a></td></tr
><tr id="gr_svn496_204"

><td id="204"><a href="#204">204</a></td></tr
><tr id="gr_svn496_205"

><td id="205"><a href="#205">205</a></td></tr
><tr id="gr_svn496_206"

><td id="206"><a href="#206">206</a></td></tr
><tr id="gr_svn496_207"

><td id="207"><a href="#207">207</a></td></tr
><tr id="gr_svn496_208"

><td id="208"><a href="#208">208</a></td></tr
><tr id="gr_svn496_209"

><td id="209"><a href="#209">209</a></td></tr
><tr id="gr_svn496_210"

><td id="210"><a href="#210">210</a></td></tr
><tr id="gr_svn496_211"

><td id="211"><a href="#211">211</a></td></tr
><tr id="gr_svn496_212"

><td id="212"><a href="#212">212</a></td></tr
><tr id="gr_svn496_213"

><td id="213"><a href="#213">213</a></td></tr
><tr id="gr_svn496_214"

><td id="214"><a href="#214">214</a></td></tr
><tr id="gr_svn496_215"

><td id="215"><a href="#215">215</a></td></tr
><tr id="gr_svn496_216"

><td id="216"><a href="#216">216</a></td></tr
><tr id="gr_svn496_217"

><td id="217"><a href="#217">217</a></td></tr
><tr id="gr_svn496_218"

><td id="218"><a href="#218">218</a></td></tr
><tr id="gr_svn496_219"

><td id="219"><a href="#219">219</a></td></tr
><tr id="gr_svn496_220"

><td id="220"><a href="#220">220</a></td></tr
><tr id="gr_svn496_221"

><td id="221"><a href="#221">221</a></td></tr
><tr id="gr_svn496_222"

><td id="222"><a href="#222">222</a></td></tr
><tr id="gr_svn496_223"

><td id="223"><a href="#223">223</a></td></tr
><tr id="gr_svn496_224"

><td id="224"><a href="#224">224</a></td></tr
><tr id="gr_svn496_225"

><td id="225"><a href="#225">225</a></td></tr
><tr id="gr_svn496_226"

><td id="226"><a href="#226">226</a></td></tr
><tr id="gr_svn496_227"

><td id="227"><a href="#227">227</a></td></tr
><tr id="gr_svn496_228"

><td id="228"><a href="#228">228</a></td></tr
><tr id="gr_svn496_229"

><td id="229"><a href="#229">229</a></td></tr
><tr id="gr_svn496_230"

><td id="230"><a href="#230">230</a></td></tr
><tr id="gr_svn496_231"

><td id="231"><a href="#231">231</a></td></tr
><tr id="gr_svn496_232"

><td id="232"><a href="#232">232</a></td></tr
><tr id="gr_svn496_233"

><td id="233"><a href="#233">233</a></td></tr
><tr id="gr_svn496_234"

><td id="234"><a href="#234">234</a></td></tr
><tr id="gr_svn496_235"

><td id="235"><a href="#235">235</a></td></tr
><tr id="gr_svn496_236"

><td id="236"><a href="#236">236</a></td></tr
><tr id="gr_svn496_237"

><td id="237"><a href="#237">237</a></td></tr
><tr id="gr_svn496_238"

><td id="238"><a href="#238">238</a></td></tr
><tr id="gr_svn496_239"

><td id="239"><a href="#239">239</a></td></tr
><tr id="gr_svn496_240"

><td id="240"><a href="#240">240</a></td></tr
><tr id="gr_svn496_241"

><td id="241"><a href="#241">241</a></td></tr
><tr id="gr_svn496_242"

><td id="242"><a href="#242">242</a></td></tr
><tr id="gr_svn496_243"

><td id="243"><a href="#243">243</a></td></tr
><tr id="gr_svn496_244"

><td id="244"><a href="#244">244</a></td></tr
><tr id="gr_svn496_245"

><td id="245"><a href="#245">245</a></td></tr
></table></pre>

<pre><table width="100%" id="nums_table_1"><tr id="gr_svn496_246"

><td id="246"><a href="#246">246</a></td></tr
><tr id="gr_svn496_247"

><td id="247"><a href="#247">247</a></td></tr
><tr id="gr_svn496_248"

><td id="248"><a href="#248">248</a></td></tr
><tr id="gr_svn496_249"

><td id="249"><a href="#249">249</a></td></tr
><tr id="gr_svn496_250"

><td id="250"><a href="#250">250</a></td></tr
><tr id="gr_svn496_251"

><td id="251"><a href="#251">251</a></td></tr
><tr id="gr_svn496_252"

><td id="252"><a href="#252">252</a></td></tr
><tr id="gr_svn496_253"

><td id="253"><a href="#253">253</a></td></tr
><tr id="gr_svn496_254"

><td id="254"><a href="#254">254</a></td></tr
><tr id="gr_svn496_255"

><td id="255"><a href="#255">255</a></td></tr
><tr id="gr_svn496_256"

><td id="256"><a href="#256">256</a></td></tr
><tr id="gr_svn496_257"

><td id="257"><a href="#257">257</a></td></tr
><tr id="gr_svn496_258"

><td id="258"><a href="#258">258</a></td></tr
><tr id="gr_svn496_259"

><td id="259"><a href="#259">259</a></td></tr
><tr id="gr_svn496_260"

><td id="260"><a href="#260">260</a></td></tr
><tr id="gr_svn496_261"

><td id="261"><a href="#261">261</a></td></tr
><tr id="gr_svn496_262"

><td id="262"><a href="#262">262</a></td></tr
><tr id="gr_svn496_263"

><td id="263"><a href="#263">263</a></td></tr
><tr id="gr_svn496_264"

><td id="264"><a href="#264">264</a></td></tr
><tr id="gr_svn496_265"

><td id="265"><a href="#265">265</a></td></tr
><tr id="gr_svn496_266"

><td id="266"><a href="#266">266</a></td></tr
><tr id="gr_svn496_267"

><td id="267"><a href="#267">267</a></td></tr
><tr id="gr_svn496_268"

><td id="268"><a href="#268">268</a></td></tr
><tr id="gr_svn496_269"

><td id="269"><a href="#269">269</a></td></tr
><tr id="gr_svn496_270"

><td id="270"><a href="#270">270</a></td></tr
><tr id="gr_svn496_271"

><td id="271"><a href="#271">271</a></td></tr
><tr id="gr_svn496_272"

><td id="272"><a href="#272">272</a></td></tr
><tr id="gr_svn496_273"

><td id="273"><a href="#273">273</a></td></tr
><tr id="gr_svn496_274"

><td id="274"><a href="#274">274</a></td></tr
><tr id="gr_svn496_275"

><td id="275"><a href="#275">275</a></td></tr
><tr id="gr_svn496_276"

><td id="276"><a href="#276">276</a></td></tr
><tr id="gr_svn496_277"

><td id="277"><a href="#277">277</a></td></tr
><tr id="gr_svn496_278"

><td id="278"><a href="#278">278</a></td></tr
><tr id="gr_svn496_279"

><td id="279"><a href="#279">279</a></td></tr
><tr id="gr_svn496_280"

><td id="280"><a href="#280">280</a></td></tr
><tr id="gr_svn496_281"

><td id="281"><a href="#281">281</a></td></tr
><tr id="gr_svn496_282"

><td id="282"><a href="#282">282</a></td></tr
><tr id="gr_svn496_283"

><td id="283"><a href="#283">283</a></td></tr
><tr id="gr_svn496_284"

><td id="284"><a href="#284">284</a></td></tr
><tr id="gr_svn496_285"

><td id="285"><a href="#285">285</a></td></tr
><tr id="gr_svn496_286"

><td id="286"><a href="#286">286</a></td></tr
><tr id="gr_svn496_287"

><td id="287"><a href="#287">287</a></td></tr
><tr id="gr_svn496_288"

><td id="288"><a href="#288">288</a></td></tr
><tr id="gr_svn496_289"

><td id="289"><a href="#289">289</a></td></tr
><tr id="gr_svn496_290"

><td id="290"><a href="#290">290</a></td></tr
><tr id="gr_svn496_291"

><td id="291"><a href="#291">291</a></td></tr
><tr id="gr_svn496_292"

><td id="292"><a href="#292">292</a></td></tr
><tr id="gr_svn496_293"

><td id="293"><a href="#293">293</a></td></tr
><tr id="gr_svn496_294"

><td id="294"><a href="#294">294</a></td></tr
><tr id="gr_svn496_295"

><td id="295"><a href="#295">295</a></td></tr
><tr id="gr_svn496_296"

><td id="296"><a href="#296">296</a></td></tr
><tr id="gr_svn496_297"

><td id="297"><a href="#297">297</a></td></tr
><tr id="gr_svn496_298"

><td id="298"><a href="#298">298</a></td></tr
><tr id="gr_svn496_299"

><td id="299"><a href="#299">299</a></td></tr
><tr id="gr_svn496_300"

><td id="300"><a href="#300">300</a></td></tr
><tr id="gr_svn496_301"

><td id="301"><a href="#301">301</a></td></tr
><tr id="gr_svn496_302"

><td id="302"><a href="#302">302</a></td></tr
><tr id="gr_svn496_303"

><td id="303"><a href="#303">303</a></td></tr
><tr id="gr_svn496_304"

><td id="304"><a href="#304">304</a></td></tr
><tr id="gr_svn496_305"

><td id="305"><a href="#305">305</a></td></tr
><tr id="gr_svn496_306"

><td id="306"><a href="#306">306</a></td></tr
><tr id="gr_svn496_307"

><td id="307"><a href="#307">307</a></td></tr
><tr id="gr_svn496_308"

><td id="308"><a href="#308">308</a></td></tr
><tr id="gr_svn496_309"

><td id="309"><a href="#309">309</a></td></tr
><tr id="gr_svn496_310"

><td id="310"><a href="#310">310</a></td></tr
><tr id="gr_svn496_311"

><td id="311"><a href="#311">311</a></td></tr
><tr id="gr_svn496_312"

><td id="312"><a href="#312">312</a></td></tr
><tr id="gr_svn496_313"

><td id="313"><a href="#313">313</a></td></tr
><tr id="gr_svn496_314"

><td id="314"><a href="#314">314</a></td></tr
><tr id="gr_svn496_315"

><td id="315"><a href="#315">315</a></td></tr
><tr id="gr_svn496_316"

><td id="316"><a href="#316">316</a></td></tr
><tr id="gr_svn496_317"

><td id="317"><a href="#317">317</a></td></tr
><tr id="gr_svn496_318"

><td id="318"><a href="#318">318</a></td></tr
><tr id="gr_svn496_319"

><td id="319"><a href="#319">319</a></td></tr
><tr id="gr_svn496_320"

><td id="320"><a href="#320">320</a></td></tr
><tr id="gr_svn496_321"

><td id="321"><a href="#321">321</a></td></tr
><tr id="gr_svn496_322"

><td id="322"><a href="#322">322</a></td></tr
><tr id="gr_svn496_323"

><td id="323"><a href="#323">323</a></td></tr
><tr id="gr_svn496_324"

><td id="324"><a href="#324">324</a></td></tr
><tr id="gr_svn496_325"

><td id="325"><a href="#325">325</a></td></tr
><tr id="gr_svn496_326"

><td id="326"><a href="#326">326</a></td></tr
><tr id="gr_svn496_327"

><td id="327"><a href="#327">327</a></td></tr
><tr id="gr_svn496_328"

><td id="328"><a href="#328">328</a></td></tr
><tr id="gr_svn496_329"

><td id="329"><a href="#329">329</a></td></tr
><tr id="gr_svn496_330"

><td id="330"><a href="#330">330</a></td></tr
><tr id="gr_svn496_331"

><td id="331"><a href="#331">331</a></td></tr
><tr id="gr_svn496_332"

><td id="332"><a href="#332">332</a></td></tr
><tr id="gr_svn496_333"

><td id="333"><a href="#333">333</a></td></tr
><tr id="gr_svn496_334"

><td id="334"><a href="#334">334</a></td></tr
><tr id="gr_svn496_335"

><td id="335"><a href="#335">335</a></td></tr
><tr id="gr_svn496_336"

><td id="336"><a href="#336">336</a></td></tr
><tr id="gr_svn496_337"

><td id="337"><a href="#337">337</a></td></tr
><tr id="gr_svn496_338"

><td id="338"><a href="#338">338</a></td></tr
><tr id="gr_svn496_339"

><td id="339"><a href="#339">339</a></td></tr
><tr id="gr_svn496_340"

><td id="340"><a href="#340">340</a></td></tr
><tr id="gr_svn496_341"

><td id="341"><a href="#341">341</a></td></tr
><tr id="gr_svn496_342"

><td id="342"><a href="#342">342</a></td></tr
><tr id="gr_svn496_343"

><td id="343"><a href="#343">343</a></td></tr
><tr id="gr_svn496_344"

><td id="344"><a href="#344">344</a></td></tr
><tr id="gr_svn496_345"

><td id="345"><a href="#345">345</a></td></tr
><tr id="gr_svn496_346"

><td id="346"><a href="#346">346</a></td></tr
><tr id="gr_svn496_347"

><td id="347"><a href="#347">347</a></td></tr
><tr id="gr_svn496_348"

><td id="348"><a href="#348">348</a></td></tr
><tr id="gr_svn496_349"

><td id="349"><a href="#349">349</a></td></tr
><tr id="gr_svn496_350"

><td id="350"><a href="#350">350</a></td></tr
><tr id="gr_svn496_351"

><td id="351"><a href="#351">351</a></td></tr
><tr id="gr_svn496_352"

><td id="352"><a href="#352">352</a></td></tr
><tr id="gr_svn496_353"

><td id="353"><a href="#353">353</a></td></tr
><tr id="gr_svn496_354"

><td id="354"><a href="#354">354</a></td></tr
><tr id="gr_svn496_355"

><td id="355"><a href="#355">355</a></td></tr
><tr id="gr_svn496_356"

><td id="356"><a href="#356">356</a></td></tr
><tr id="gr_svn496_357"

><td id="357"><a href="#357">357</a></td></tr
><tr id="gr_svn496_358"

><td id="358"><a href="#358">358</a></td></tr
><tr id="gr_svn496_359"

><td id="359"><a href="#359">359</a></td></tr
><tr id="gr_svn496_360"

><td id="360"><a href="#360">360</a></td></tr
><tr id="gr_svn496_361"

><td id="361"><a href="#361">361</a></td></tr
><tr id="gr_svn496_362"

><td id="362"><a href="#362">362</a></td></tr
><tr id="gr_svn496_363"

><td id="363"><a href="#363">363</a></td></tr
><tr id="gr_svn496_364"

><td id="364"><a href="#364">364</a></td></tr
><tr id="gr_svn496_365"

><td id="365"><a href="#365">365</a></td></tr
><tr id="gr_svn496_366"

><td id="366"><a href="#366">366</a></td></tr
><tr id="gr_svn496_367"

><td id="367"><a href="#367">367</a></td></tr
><tr id="gr_svn496_368"

><td id="368"><a href="#368">368</a></td></tr
><tr id="gr_svn496_369"

><td id="369"><a href="#369">369</a></td></tr
><tr id="gr_svn496_370"

><td id="370"><a href="#370">370</a></td></tr
><tr id="gr_svn496_371"

><td id="371"><a href="#371">371</a></td></tr
><tr id="gr_svn496_372"

><td id="372"><a href="#372">372</a></td></tr
><tr id="gr_svn496_373"

><td id="373"><a href="#373">373</a></td></tr
><tr id="gr_svn496_374"

><td id="374"><a href="#374">374</a></td></tr
><tr id="gr_svn496_375"

><td id="375"><a href="#375">375</a></td></tr
><tr id="gr_svn496_376"

><td id="376"><a href="#376">376</a></td></tr
><tr id="gr_svn496_377"

><td id="377"><a href="#377">377</a></td></tr
><tr id="gr_svn496_378"

><td id="378"><a href="#378">378</a></td></tr
><tr id="gr_svn496_379"

><td id="379"><a href="#379">379</a></td></tr
><tr id="gr_svn496_380"

><td id="380"><a href="#380">380</a></td></tr
><tr id="gr_svn496_381"

><td id="381"><a href="#381">381</a></td></tr
><tr id="gr_svn496_382"

><td id="382"><a href="#382">382</a></td></tr
><tr id="gr_svn496_383"

><td id="383"><a href="#383">383</a></td></tr
><tr id="gr_svn496_384"

><td id="384"><a href="#384">384</a></td></tr
><tr id="gr_svn496_385"

><td id="385"><a href="#385">385</a></td></tr
><tr id="gr_svn496_386"

><td id="386"><a href="#386">386</a></td></tr
><tr id="gr_svn496_387"

><td id="387"><a href="#387">387</a></td></tr
><tr id="gr_svn496_388"

><td id="388"><a href="#388">388</a></td></tr
><tr id="gr_svn496_389"

><td id="389"><a href="#389">389</a></td></tr
><tr id="gr_svn496_390"

><td id="390"><a href="#390">390</a></td></tr
><tr id="gr_svn496_391"

><td id="391"><a href="#391">391</a></td></tr
><tr id="gr_svn496_392"

><td id="392"><a href="#392">392</a></td></tr
><tr id="gr_svn496_393"

><td id="393"><a href="#393">393</a></td></tr
><tr id="gr_svn496_394"

><td id="394"><a href="#394">394</a></td></tr
><tr id="gr_svn496_395"

><td id="395"><a href="#395">395</a></td></tr
><tr id="gr_svn496_396"

><td id="396"><a href="#396">396</a></td></tr
><tr id="gr_svn496_397"

><td id="397"><a href="#397">397</a></td></tr
><tr id="gr_svn496_398"

><td id="398"><a href="#398">398</a></td></tr
><tr id="gr_svn496_399"

><td id="399"><a href="#399">399</a></td></tr
><tr id="gr_svn496_400"

><td id="400"><a href="#400">400</a></td></tr
><tr id="gr_svn496_401"

><td id="401"><a href="#401">401</a></td></tr
><tr id="gr_svn496_402"

><td id="402"><a href="#402">402</a></td></tr
><tr id="gr_svn496_403"

><td id="403"><a href="#403">403</a></td></tr
><tr id="gr_svn496_404"

><td id="404"><a href="#404">404</a></td></tr
><tr id="gr_svn496_405"

><td id="405"><a href="#405">405</a></td></tr
><tr id="gr_svn496_406"

><td id="406"><a href="#406">406</a></td></tr
><tr id="gr_svn496_407"

><td id="407"><a href="#407">407</a></td></tr
><tr id="gr_svn496_408"

><td id="408"><a href="#408">408</a></td></tr
><tr id="gr_svn496_409"

><td id="409"><a href="#409">409</a></td></tr
><tr id="gr_svn496_410"

><td id="410"><a href="#410">410</a></td></tr
><tr id="gr_svn496_411"

><td id="411"><a href="#411">411</a></td></tr
><tr id="gr_svn496_412"

><td id="412"><a href="#412">412</a></td></tr
><tr id="gr_svn496_413"

><td id="413"><a href="#413">413</a></td></tr
><tr id="gr_svn496_414"

><td id="414"><a href="#414">414</a></td></tr
><tr id="gr_svn496_415"

><td id="415"><a href="#415">415</a></td></tr
><tr id="gr_svn496_416"

><td id="416"><a href="#416">416</a></td></tr
><tr id="gr_svn496_417"

><td id="417"><a href="#417">417</a></td></tr
><tr id="gr_svn496_418"

><td id="418"><a href="#418">418</a></td></tr
><tr id="gr_svn496_419"

><td id="419"><a href="#419">419</a></td></tr
><tr id="gr_svn496_420"

><td id="420"><a href="#420">420</a></td></tr
><tr id="gr_svn496_421"

><td id="421"><a href="#421">421</a></td></tr
><tr id="gr_svn496_422"

><td id="422"><a href="#422">422</a></td></tr
><tr id="gr_svn496_423"

><td id="423"><a href="#423">423</a></td></tr
><tr id="gr_svn496_424"

><td id="424"><a href="#424">424</a></td></tr
><tr id="gr_svn496_425"

><td id="425"><a href="#425">425</a></td></tr
><tr id="gr_svn496_426"

><td id="426"><a href="#426">426</a></td></tr
><tr id="gr_svn496_427"

><td id="427"><a href="#427">427</a></td></tr
><tr id="gr_svn496_428"

><td id="428"><a href="#428">428</a></td></tr
><tr id="gr_svn496_429"

><td id="429"><a href="#429">429</a></td></tr
><tr id="gr_svn496_430"

><td id="430"><a href="#430">430</a></td></tr
><tr id="gr_svn496_431"

><td id="431"><a href="#431">431</a></td></tr
><tr id="gr_svn496_432"

><td id="432"><a href="#432">432</a></td></tr
><tr id="gr_svn496_433"

><td id="433"><a href="#433">433</a></td></tr
><tr id="gr_svn496_434"

><td id="434"><a href="#434">434</a></td></tr
><tr id="gr_svn496_435"

><td id="435"><a href="#435">435</a></td></tr
><tr id="gr_svn496_436"

><td id="436"><a href="#436">436</a></td></tr
><tr id="gr_svn496_437"

><td id="437"><a href="#437">437</a></td></tr
><tr id="gr_svn496_438"

><td id="438"><a href="#438">438</a></td></tr
><tr id="gr_svn496_439"

><td id="439"><a href="#439">439</a></td></tr
><tr id="gr_svn496_440"

><td id="440"><a href="#440">440</a></td></tr
><tr id="gr_svn496_441"

><td id="441"><a href="#441">441</a></td></tr
><tr id="gr_svn496_442"

><td id="442"><a href="#442">442</a></td></tr
><tr id="gr_svn496_443"

><td id="443"><a href="#443">443</a></td></tr
><tr id="gr_svn496_444"

><td id="444"><a href="#444">444</a></td></tr
><tr id="gr_svn496_445"

><td id="445"><a href="#445">445</a></td></tr
><tr id="gr_svn496_446"

><td id="446"><a href="#446">446</a></td></tr
><tr id="gr_svn496_447"

><td id="447"><a href="#447">447</a></td></tr
><tr id="gr_svn496_448"

><td id="448"><a href="#448">448</a></td></tr
><tr id="gr_svn496_449"

><td id="449"><a href="#449">449</a></td></tr
><tr id="gr_svn496_450"

><td id="450"><a href="#450">450</a></td></tr
><tr id="gr_svn496_451"

><td id="451"><a href="#451">451</a></td></tr
><tr id="gr_svn496_452"

><td id="452"><a href="#452">452</a></td></tr
><tr id="gr_svn496_453"

><td id="453"><a href="#453">453</a></td></tr
><tr id="gr_svn496_454"

><td id="454"><a href="#454">454</a></td></tr
><tr id="gr_svn496_455"

><td id="455"><a href="#455">455</a></td></tr
><tr id="gr_svn496_456"

><td id="456"><a href="#456">456</a></td></tr
><tr id="gr_svn496_457"

><td id="457"><a href="#457">457</a></td></tr
><tr id="gr_svn496_458"

><td id="458"><a href="#458">458</a></td></tr
><tr id="gr_svn496_459"

><td id="459"><a href="#459">459</a></td></tr
></table></pre>

<pre><table width="100%" id="nums_table_2"><tr id="gr_svn496_460"

><td id="460"><a href="#460">460</a></td></tr
><tr id="gr_svn496_461"

><td id="461"><a href="#461">461</a></td></tr
><tr id="gr_svn496_462"

><td id="462"><a href="#462">462</a></td></tr
><tr id="gr_svn496_463"

><td id="463"><a href="#463">463</a></td></tr
><tr id="gr_svn496_464"

><td id="464"><a href="#464">464</a></td></tr
><tr id="gr_svn496_465"

><td id="465"><a href="#465">465</a></td></tr
><tr id="gr_svn496_466"

><td id="466"><a href="#466">466</a></td></tr
><tr id="gr_svn496_467"

><td id="467"><a href="#467">467</a></td></tr
><tr id="gr_svn496_468"

><td id="468"><a href="#468">468</a></td></tr
><tr id="gr_svn496_469"

><td id="469"><a href="#469">469</a></td></tr
><tr id="gr_svn496_470"

><td id="470"><a href="#470">470</a></td></tr
><tr id="gr_svn496_471"

><td id="471"><a href="#471">471</a></td></tr
><tr id="gr_svn496_472"

><td id="472"><a href="#472">472</a></td></tr
><tr id="gr_svn496_473"

><td id="473"><a href="#473">473</a></td></tr
><tr id="gr_svn496_474"

><td id="474"><a href="#474">474</a></td></tr
><tr id="gr_svn496_475"

><td id="475"><a href="#475">475</a></td></tr
><tr id="gr_svn496_476"

><td id="476"><a href="#476">476</a></td></tr
><tr id="gr_svn496_477"

><td id="477"><a href="#477">477</a></td></tr
><tr id="gr_svn496_478"

><td id="478"><a href="#478">478</a></td></tr
><tr id="gr_svn496_479"

><td id="479"><a href="#479">479</a></td></tr
><tr id="gr_svn496_480"

><td id="480"><a href="#480">480</a></td></tr
><tr id="gr_svn496_481"

><td id="481"><a href="#481">481</a></td></tr
><tr id="gr_svn496_482"

><td id="482"><a href="#482">482</a></td></tr
><tr id="gr_svn496_483"

><td id="483"><a href="#483">483</a></td></tr
><tr id="gr_svn496_484"

><td id="484"><a href="#484">484</a></td></tr
><tr id="gr_svn496_485"

><td id="485"><a href="#485">485</a></td></tr
><tr id="gr_svn496_486"

><td id="486"><a href="#486">486</a></td></tr
><tr id="gr_svn496_487"

><td id="487"><a href="#487">487</a></td></tr
><tr id="gr_svn496_488"

><td id="488"><a href="#488">488</a></td></tr
><tr id="gr_svn496_489"

><td id="489"><a href="#489">489</a></td></tr
><tr id="gr_svn496_490"

><td id="490"><a href="#490">490</a></td></tr
><tr id="gr_svn496_491"

><td id="491"><a href="#491">491</a></td></tr
><tr id="gr_svn496_492"

><td id="492"><a href="#492">492</a></td></tr
><tr id="gr_svn496_493"

><td id="493"><a href="#493">493</a></td></tr
></table></pre>

<pre><table width="100%"><tr class="nocursor"><td></td></tr></table></pre>
</td>
<td id="lines">
<pre class="prettyprint"><table width="100%"><tr class="cursor_stop cursor_hidden"><td></td></tr></table></pre>

<pre class="prettyprint lang-py"><table id="src_table_0"><tr
id=sl_svn496_1

><td class="source"># -*- coding: cp1252 -*-<br></td></tr
><tr
id=sl_svn496_2

><td class="source"># (c) Marcelo Barros de Almeida<br></td></tr
><tr
id=sl_svn496_3

><td class="source"># marcelobarrosalmeida@gmail.com<br></td></tr
><tr
id=sl_svn496_4

><td class="source"># License: GPL3<br></td></tr
><tr
id=sl_svn496_5

><td class="source"><br></td></tr
><tr
id=sl_svn496_6

><td class="source">from appuifw import *<br></td></tr
><tr
id=sl_svn496_7

><td class="source">import e32<br></td></tr
><tr
id=sl_svn496_8

><td class="source">import sysinfo<br></td></tr
><tr
id=sl_svn496_9

><td class="source">import os<br></td></tr
><tr
id=sl_svn496_10

><td class="source">import graphics<br></td></tr
><tr
id=sl_svn496_11

><td class="source">import key_codes<br></td></tr
><tr
id=sl_svn496_12

><td class="source">from math import ceil, floor<br></td></tr
><tr
id=sl_svn496_13

><td class="source"><br></td></tr
><tr
id=sl_svn496_14

><td class="source">class CanvasListBox(Canvas):<br></td></tr
><tr
id=sl_svn496_15

><td class="source">    &quot;&quot;&quot; This classes creates a listbox with variable row size on canvas.<br></td></tr
><tr
id=sl_svn496_16

><td class="source">    &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_17

><td class="source">    def __init__(self,**attrs):<br></td></tr
><tr
id=sl_svn496_18

><td class="source">        &quot;&quot;&quot; Creates a list box on canvas. Just fill the desired parameters attributes.<br></td></tr
><tr
id=sl_svn496_19

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_20

><td class="source">        Canvas.__init__(self,<br></td></tr
><tr
id=sl_svn496_21

><td class="source">                        redraw_callback = self.redraw_list,<br></td></tr
><tr
id=sl_svn496_22

><td class="source">                        event_callback = self.event_list)<br></td></tr
><tr
id=sl_svn496_23

><td class="source">        self.check_default_values(attrs)<br></td></tr
><tr
id=sl_svn496_24

><td class="source">        self.set_binds(True)<br></td></tr
><tr
id=sl_svn496_25

><td class="source"><br></td></tr
><tr
id=sl_svn496_26

><td class="source">    def set_binds(self,val):<br></td></tr
><tr
id=sl_svn496_27

><td class="source">        &quot;&quot;&quot; Enable or disable bindings<br></td></tr
><tr
id=sl_svn496_28

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_29

><td class="source">        if val:<br></td></tr
><tr
id=sl_svn496_30

><td class="source">            self.bind(key_codes.EKeyUpArrow, self.up_key)<br></td></tr
><tr
id=sl_svn496_31

><td class="source">            self.bind(key_codes.EKeyDownArrow, self.down_key)<br></td></tr
><tr
id=sl_svn496_32

><td class="source">            self.bind(key_codes.EKeySelect, self.attrs[&#39;cbk&#39;])<br></td></tr
><tr
id=sl_svn496_33

><td class="source">        else:<br></td></tr
><tr
id=sl_svn496_34

><td class="source">            self.bind(key_codes.EKeyUpArrow, None)<br></td></tr
><tr
id=sl_svn496_35

><td class="source">            self.bind(key_codes.EKeyDownArrow, None)<br></td></tr
><tr
id=sl_svn496_36

><td class="source">            self.bind(key_codes.EKeySelect, None)<br></td></tr
><tr
id=sl_svn496_37

><td class="source"><br></td></tr
><tr
id=sl_svn496_38

><td class="source">    def get_config(self):<br></td></tr
><tr
id=sl_svn496_39

><td class="source">        &quot;&quot;&quot; Return listbox attributes<br></td></tr
><tr
id=sl_svn496_40

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_41

><td class="source">        return self.attrs<br></td></tr
><tr
id=sl_svn496_42

><td class="source">    <br></td></tr
><tr
id=sl_svn496_43

><td class="source">    def check_default_values(self,attrs):<br></td></tr
><tr
id=sl_svn496_44

><td class="source">        &quot;&quot;&quot; Given some user attributes, define all listbox attributes<br></td></tr
><tr
id=sl_svn496_45

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_46

><td class="source">        self.attrs = {}<br></td></tr
><tr
id=sl_svn496_47

><td class="source">        self.def_attrs = {&#39;items&#39;:[],<br></td></tr
><tr
id=sl_svn496_48

><td class="source">                          &#39;cbk&#39;:lambda:None,<br></td></tr
><tr
id=sl_svn496_49

><td class="source">                          &#39;position&#39;:(0,0,self.size[0],self.size[1]),<br></td></tr
><tr
id=sl_svn496_50

><td class="source">                          &#39;scrollbar_width&#39;:5,<br></td></tr
><tr
id=sl_svn496_51

><td class="source">                          &#39;margins&#39;:(2,2,2,2),<br></td></tr
><tr
id=sl_svn496_52

><td class="source">                          &#39;font_name&#39;:&#39;dense&#39;,<br></td></tr
><tr
id=sl_svn496_53

><td class="source">                          &#39;font_color&#39;:(255,255,255),<br></td></tr
><tr
id=sl_svn496_54

><td class="source">                          &#39;font_fill_color&#39;:(0,0,0),<br></td></tr
><tr
id=sl_svn496_55

><td class="source">                          &#39;line_space&#39;: 0,<br></td></tr
><tr
id=sl_svn496_56

><td class="source">                          &#39;line_break_chars&#39;:u&quot; .;:\\/-&quot;,<br></td></tr
><tr
id=sl_svn496_57

><td class="source">                          &#39;scrollbar_color&#39;:(255,255,255),<br></td></tr
><tr
id=sl_svn496_58

><td class="source">                          &#39;selection_font_color&#39;:(255,255,102),<br></td></tr
><tr
id=sl_svn496_59

><td class="source">                          &#39;selection_fill_color&#39;:(124,104,238),<br></td></tr
><tr
id=sl_svn496_60

><td class="source">                          &#39;selection_border_color&#39;:(255,255,102),<br></td></tr
><tr
id=sl_svn496_61

><td class="source">                          &#39;odd_fill_color&#39;:(0,0,0),<br></td></tr
><tr
id=sl_svn496_62

><td class="source">                          &#39;even_fill_color&#39;:(50,50,50),<br></td></tr
><tr
id=sl_svn496_63

><td class="source">                          &#39;images&#39;:[],<br></td></tr
><tr
id=sl_svn496_64

><td class="source">                          &#39;image_size&#39;:(44,44),<br></td></tr
><tr
id=sl_svn496_65

><td class="source">                          &#39;image_keep_aspect&#39;:1,<br></td></tr
><tr
id=sl_svn496_66

><td class="source">                          &#39;image_margin&#39;:0,<br></td></tr
><tr
id=sl_svn496_67

><td class="source">                          &#39;title&#39;:u&quot;&quot;,<br></td></tr
><tr
id=sl_svn496_68

><td class="source">                          &#39;title_font&#39;:&#39;dense&#39;,<br></td></tr
><tr
id=sl_svn496_69

><td class="source">                          &#39;title_font_color&#39;:(255,255,102),<br></td></tr
><tr
id=sl_svn496_70

><td class="source">                          &#39;title_fill_color&#39;:(124,104,238),<br></td></tr
><tr
id=sl_svn496_71

><td class="source">                          &#39;title_border_color&#39;:(124,104,238)}<br></td></tr
><tr
id=sl_svn496_72

><td class="source">        <br></td></tr
><tr
id=sl_svn496_73

><td class="source">        for k in self.def_attrs.keys():<br></td></tr
><tr
id=sl_svn496_74

><td class="source">            if attrs.has_key(k):<br></td></tr
><tr
id=sl_svn496_75

><td class="source">                self.attrs[k] = attrs[k]<br></td></tr
><tr
id=sl_svn496_76

><td class="source">            else:<br></td></tr
><tr
id=sl_svn496_77

><td class="source">                self.attrs[k] = self.def_attrs[k]<br></td></tr
><tr
id=sl_svn496_78

><td class="source">        # fixing spacing<br></td></tr
><tr
id=sl_svn496_79

><td class="source">        fh = -(graphics.Image.new((1,1)).measure_text(&quot;[qg_|^y&quot;,font=self.attrs[&#39;font_name&#39;])[0][1])<br></td></tr
><tr
id=sl_svn496_80

><td class="source">        self.attrs[&#39;font_height&#39;] = fh<br></td></tr
><tr
id=sl_svn496_81

><td class="source">        self.attrs[&#39;line_space&#39;] = max(3,fh/4,self.attrs[&#39;line_space&#39;])<br></td></tr
><tr
id=sl_svn496_82

><td class="source">        # translating to origin (0,0)<br></td></tr
><tr
id=sl_svn496_83

><td class="source">        self.position = (0,<br></td></tr
><tr
id=sl_svn496_84

><td class="source">                         0,<br></td></tr
><tr
id=sl_svn496_85

><td class="source">                         self.attrs[&#39;position&#39;][2] - self.attrs[&#39;position&#39;][0],<br></td></tr
><tr
id=sl_svn496_86

><td class="source">                         self.attrs[&#39;position&#39;][3] - self.attrs[&#39;position&#39;][1])<br></td></tr
><tr
id=sl_svn496_87

><td class="source">        # no images, no border<br></td></tr
><tr
id=sl_svn496_88

><td class="source">        if not self.attrs[&#39;images&#39;]:<br></td></tr
><tr
id=sl_svn496_89

><td class="source">            self.attrs[&#39;image_size&#39;] = (0,0)<br></td></tr
><tr
id=sl_svn496_90

><td class="source">        # if we have a title, add additional space for it<br></td></tr
><tr
id=sl_svn496_91

><td class="source">        if self.attrs[&#39;title&#39;]:<br></td></tr
><tr
id=sl_svn496_92

><td class="source">            self.attrs[&#39;title_position&#39;]=(0,<br></td></tr
><tr
id=sl_svn496_93

><td class="source">                                          0,<br></td></tr
><tr
id=sl_svn496_94

><td class="source">                                          self.position[2],<br></td></tr
><tr
id=sl_svn496_95

><td class="source">                                          self.attrs[&#39;font_height&#39;]+2*self.attrs[&#39;line_space&#39;])<br></td></tr
><tr
id=sl_svn496_96

><td class="source">        else:<br></td></tr
><tr
id=sl_svn496_97

><td class="source">            self.attrs[&#39;title_position&#39;]=(0,0,0,0)<br></td></tr
><tr
id=sl_svn496_98

><td class="source">            <br></td></tr
><tr
id=sl_svn496_99

><td class="source">        # img_margin + img_size + text_margin<br></td></tr
><tr
id=sl_svn496_100

><td class="source">        self.lstbox_xa = self.position[0] + self.attrs[&#39;margins&#39;][0] + \<br></td></tr
><tr
id=sl_svn496_101

><td class="source">                         self.attrs[&#39;image_size&#39;][0] + self.attrs[&#39;image_margin&#39;]<br></td></tr
><tr
id=sl_svn496_102

><td class="source">        self.lstbox_ya = self.position[1] + self.attrs[&#39;margins&#39;][1] + \<br></td></tr
><tr
id=sl_svn496_103

><td class="source">                         self.attrs[&#39;title_position&#39;][3]<br></td></tr
><tr
id=sl_svn496_104

><td class="source">        self.lstbox_xb = self.position[2] - self.attrs[&#39;margins&#39;][2] - \<br></td></tr
><tr
id=sl_svn496_105

><td class="source">                         self.attrs[&#39;scrollbar_width&#39;]<br></td></tr
><tr
id=sl_svn496_106

><td class="source">        self.lstbox_yb = self.position[3] - self.attrs[&#39;margins&#39;][3]<br></td></tr
><tr
id=sl_svn496_107

><td class="source">        <br></td></tr
><tr
id=sl_svn496_108

><td class="source">        self.scrbar_xa = self.position[2] - self.attrs[&#39;scrollbar_width&#39;]<br></td></tr
><tr
id=sl_svn496_109

><td class="source">        self.scrbar_ya = self.position[1] + self.attrs[&#39;title_position&#39;][3]<br></td></tr
><tr
id=sl_svn496_110

><td class="source">        self.scrbar_xb = self.position[2]<br></td></tr
><tr
id=sl_svn496_111

><td class="source">        self.scrbar_yb = self.position[3]<br></td></tr
><tr
id=sl_svn496_112

><td class="source"><br></td></tr
><tr
id=sl_svn496_113

><td class="source">        self.images_xa = self.position[0] + self.attrs[&#39;image_margin&#39;]<br></td></tr
><tr
id=sl_svn496_114

><td class="source"><br></td></tr
><tr
id=sl_svn496_115

><td class="source">        self.selbox_xa = self.position[0]<br></td></tr
><tr
id=sl_svn496_116

><td class="source">        self.selbox_xb = self.position[2] - self.attrs[&#39;scrollbar_width&#39;]<br></td></tr
><tr
id=sl_svn496_117

><td class="source"><br></td></tr
><tr
id=sl_svn496_118

><td class="source">        self.lstbox_size = (self.position[2]-self.position[0],<br></td></tr
><tr
id=sl_svn496_119

><td class="source">                            self.position[3]-self.position[1])<br></td></tr
><tr
id=sl_svn496_120

><td class="source">        self._screen = graphics.Image.new(self.lstbox_size)<br></td></tr
><tr
id=sl_svn496_121

><td class="source"><br></td></tr
><tr
id=sl_svn496_122

><td class="source">        # selected item. It is relative to 0.<br></td></tr
><tr
id=sl_svn496_123

><td class="source">        self._current_sel = 0<br></td></tr
><tr
id=sl_svn496_124

><td class="source">        # current selection inside view. It is relative<br></td></tr
><tr
id=sl_svn496_125

><td class="source">        # to the view (self._selection_view[0]).<br></td></tr
><tr
id=sl_svn496_126

><td class="source">        self._current_sel_in_view = 0<br></td></tr
><tr
id=sl_svn496_127

><td class="source">        # current items in the view. It is relative to 0<br></td></tr
><tr
id=sl_svn496_128

><td class="source">        self._selection_view = [0,0]<br></td></tr
><tr
id=sl_svn496_129

><td class="source">        # save original data<br></td></tr
><tr
id=sl_svn496_130

><td class="source">        self._items = self.attrs[&#39;items&#39;]<br></td></tr
><tr
id=sl_svn496_131

><td class="source">        self.build_list(self.attrs[&#39;items&#39;])        <br></td></tr
><tr
id=sl_svn496_132

><td class="source">        self.calculate_sel_view()<br></td></tr
><tr
id=sl_svn496_133

><td class="source">        self.redraw_list()<br></td></tr
><tr
id=sl_svn496_134

><td class="source">        <br></td></tr
><tr
id=sl_svn496_135

><td class="source">    def reconfigure(self,attrs={}):<br></td></tr
><tr
id=sl_svn496_136

><td class="source">        &quot;&quot;&quot; Given some user attributes, define e reconfigure all listbox attributes<br></td></tr
><tr
id=sl_svn496_137

><td class="source">        &quot;&quot;&quot;        <br></td></tr
><tr
id=sl_svn496_138

><td class="source">        self.check_default_values(attrs)<br></td></tr
><tr
id=sl_svn496_139

><td class="source">        <br></td></tr
><tr
id=sl_svn496_140

><td class="source">    def redraw_list(self,rect=None):<br></td></tr
><tr
id=sl_svn496_141

><td class="source">        &quot;&quot;&quot; Redraw the listbox. This routine only updates the listbox area, defined<br></td></tr
><tr
id=sl_svn496_142

><td class="source">            self.attrs[&#39;position&#39;]<br></td></tr
><tr
id=sl_svn496_143

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_144

><td class="source">        self.set_binds(False) # it is necessary to disable bindings since redrawing may takes a long time<br></td></tr
><tr
id=sl_svn496_145

><td class="source">        self.clear_list()<br></td></tr
><tr
id=sl_svn496_146

><td class="source">        self.draw_title()<br></td></tr
><tr
id=sl_svn496_147

><td class="source">        self.draw_scroll_bar()<br></td></tr
><tr
id=sl_svn496_148

><td class="source">        self.redraw_items()<br></td></tr
><tr
id=sl_svn496_149

><td class="source">        self.blit(self._screen,<br></td></tr
><tr
id=sl_svn496_150

><td class="source">                  target=(self.attrs[&#39;position&#39;][0],self.attrs[&#39;position&#39;][1]),<br></td></tr
><tr
id=sl_svn496_151

><td class="source">                  source=((0,0),self.lstbox_size))<br></td></tr
><tr
id=sl_svn496_152

><td class="source">        self.set_binds(True)<br></td></tr
><tr
id=sl_svn496_153

><td class="source"><br></td></tr
><tr
id=sl_svn496_154

><td class="source">    def draw_title(self):<br></td></tr
><tr
id=sl_svn496_155

><td class="source">        &quot;&quot;&quot; If a title was specified, redraw it<br></td></tr
><tr
id=sl_svn496_156

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_157

><td class="source">        if self.attrs[&#39;title&#39;]:<br></td></tr
><tr
id=sl_svn496_158

><td class="source">            self._screen.rectangle((self.attrs[&#39;title_position&#39;]),<br></td></tr
><tr
id=sl_svn496_159

><td class="source">                                   outline = self.attrs[&#39;title_border_color&#39;],<br></td></tr
><tr
id=sl_svn496_160

><td class="source">                                   fill = self.attrs[&#39;title_fill_color&#39;])  <br></td></tr
><tr
id=sl_svn496_161

><td class="source">            self._screen.text((self.attrs[&#39;title_position&#39;][0],<br></td></tr
><tr
id=sl_svn496_162

><td class="source">                               self.attrs[&#39;title_position&#39;][1]+<br></td></tr
><tr
id=sl_svn496_163

><td class="source">                               self.attrs[&#39;font_height&#39;]+<br></td></tr
><tr
id=sl_svn496_164

><td class="source">                               self.attrs[&#39;line_space&#39;]),<br></td></tr
><tr
id=sl_svn496_165

><td class="source">                              self.attrs[&#39;title&#39;],<br></td></tr
><tr
id=sl_svn496_166

><td class="source">                              fill=self.attrs[&#39;title_font_color&#39;],<br></td></tr
><tr
id=sl_svn496_167

><td class="source">                              font=self.attrs[&#39;title_font&#39;])<br></td></tr
><tr
id=sl_svn496_168

><td class="source">            <br></td></tr
><tr
id=sl_svn496_169

><td class="source">    def draw_scroll_bar(self):<br></td></tr
><tr
id=sl_svn496_170

><td class="source">        &quot;&quot;&quot; Draw the scroolbar<br></td></tr
><tr
id=sl_svn496_171

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_172

><td class="source">        self._screen.rectangle((self.scrbar_xa,<br></td></tr
><tr
id=sl_svn496_173

><td class="source">                                self.scrbar_ya,<br></td></tr
><tr
id=sl_svn496_174

><td class="source">                                self.scrbar_xb,<br></td></tr
><tr
id=sl_svn496_175

><td class="source">                                self.scrbar_yb),<br></td></tr
><tr
id=sl_svn496_176

><td class="source">                               outline = self.attrs[&#39;scrollbar_color&#39;])<br></td></tr
><tr
id=sl_svn496_177

><td class="source">        list_size = len(self.lstbox_items)<br></td></tr
><tr
id=sl_svn496_178

><td class="source">        if list_size:<br></td></tr
><tr
id=sl_svn496_179

><td class="source">            pos = self.scrbar_ya + self._current_sel*(self.scrbar_yb-<br></td></tr
><tr
id=sl_svn496_180

><td class="source">                                                      self.scrbar_ya)/float(list_size)<br></td></tr
><tr
id=sl_svn496_181

><td class="source">            pos = int(pos)<br></td></tr
><tr
id=sl_svn496_182

><td class="source">            pos_ya = max(self.scrbar_ya,pos-10)<br></td></tr
><tr
id=sl_svn496_183

><td class="source">            pos_yb = min(self.scrbar_yb,pos+10)<br></td></tr
><tr
id=sl_svn496_184

><td class="source">            self._screen.rectangle((self.scrbar_xa, pos_ya, self.scrbar_xb, pos_yb),<br></td></tr
><tr
id=sl_svn496_185

><td class="source">                                   outline = self.attrs[&#39;scrollbar_color&#39;],<br></td></tr
><tr
id=sl_svn496_186

><td class="source">                                   fill = self.attrs[&#39;scrollbar_color&#39;])            <br></td></tr
><tr
id=sl_svn496_187

><td class="source"><br></td></tr
><tr
id=sl_svn496_188

><td class="source">    def redraw_items(self):<br></td></tr
><tr
id=sl_svn496_189

><td class="source">        &quot;&quot;&quot; Redraw current visible listbox items<br></td></tr
><tr
id=sl_svn496_190

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_191

><td class="source">        xa = self.lstbox_xa<br></td></tr
><tr
id=sl_svn496_192

><td class="source">        xb = self.lstbox_xb<br></td></tr
><tr
id=sl_svn496_193

><td class="source">        y = self.lstbox_ya + self.attrs[&#39;font_height&#39;]<br></td></tr
><tr
id=sl_svn496_194

><td class="source">        ysa = self.lstbox_ya<br></td></tr
><tr
id=sl_svn496_195

><td class="source">        n = self._selection_view[0]<br></td></tr
><tr
id=sl_svn496_196

><td class="source">        while y &lt; self.lstbox_yb and n &lt; len(self.lstbox_items):<br></td></tr
><tr
id=sl_svn496_197

><td class="source">            row = self.lstbox_items[n]<br></td></tr
><tr
id=sl_svn496_198

><td class="source">            # select fill color<br></td></tr
><tr
id=sl_svn496_199

><td class="source">            ysb = ysa + row[&#39;height&#39;]<br></td></tr
><tr
id=sl_svn496_200

><td class="source">            font_color = self.attrs[&#39;font_color&#39;]<br></td></tr
><tr
id=sl_svn496_201

><td class="source">            if n == self._current_sel:<br></td></tr
><tr
id=sl_svn496_202

><td class="source">                font_color = self.attrs[&#39;selection_font_color&#39;]<br></td></tr
><tr
id=sl_svn496_203

><td class="source">                # selection at center<br></td></tr
><tr
id=sl_svn496_204

><td class="source">                pos = (self.selbox_xa,ysa-int(ceil(self.attrs[&#39;line_space&#39;]/2)),<br></td></tr
><tr
id=sl_svn496_205

><td class="source">                       self.selbox_xb,ysb + 1 -int(floor(self.attrs[&#39;line_space&#39;]/2)))<br></td></tr
><tr
id=sl_svn496_206

><td class="source">                outline = self.attrs[&#39;selection_border_color&#39;]<br></td></tr
><tr
id=sl_svn496_207

><td class="source">                fill = fill = self.attrs[&#39;selection_fill_color&#39;]<br></td></tr
><tr
id=sl_svn496_208

><td class="source">            elif n % 2:<br></td></tr
><tr
id=sl_svn496_209

><td class="source">                pos = (self.selbox_xa,ysa,self.selbox_xb,ysb)<br></td></tr
><tr
id=sl_svn496_210

><td class="source">                outline = self.attrs[&#39;odd_fill_color&#39;]<br></td></tr
><tr
id=sl_svn496_211

><td class="source">                fill = self.attrs[&#39;odd_fill_color&#39;]<br></td></tr
><tr
id=sl_svn496_212

><td class="source">            else:<br></td></tr
><tr
id=sl_svn496_213

><td class="source">                pos = (self.selbox_xa,ysa,self.selbox_xb,ysb)<br></td></tr
><tr
id=sl_svn496_214

><td class="source">                outline = self.attrs[&#39;even_fill_color&#39;]<br></td></tr
><tr
id=sl_svn496_215

><td class="source">                fill = self.attrs[&#39;even_fill_color&#39;]<br></td></tr
><tr
id=sl_svn496_216

><td class="source">            self._screen.rectangle(pos,outline = outline,fill = fill)<br></td></tr
><tr
id=sl_svn496_217

><td class="source">            ysa = ysb<br></td></tr
><tr
id=sl_svn496_218

><td class="source">            # draw image, if any<br></td></tr
><tr
id=sl_svn496_219

><td class="source">            if row[&#39;file&#39;]:<br></td></tr
><tr
id=sl_svn496_220

><td class="source">                if not row[&#39;image&#39;]: # loading image only when necessary<br></td></tr
><tr
id=sl_svn496_221

><td class="source">                    try:<br></td></tr
><tr
id=sl_svn496_222

><td class="source">                        row[&#39;image&#39;] = graphics.Image.open(row[&#39;file&#39;])<br></td></tr
><tr
id=sl_svn496_223

><td class="source">                        if row[&#39;image&#39;].size[0] &gt; self.attrs[&#39;image_size&#39;][0] or \<br></td></tr
><tr
id=sl_svn496_224

><td class="source">                           row[&#39;image&#39;].size[1] &gt; self.attrs[&#39;image_size&#39;][1]:<br></td></tr
><tr
id=sl_svn496_225

><td class="source">                            row[&#39;image&#39;] = row[&#39;image&#39;].resize(self.attrs[&#39;image_size&#39;],<br></td></tr
><tr
id=sl_svn496_226

><td class="source">                                                               keepaspect=self.attrs[&#39;image_keep_aspect&#39;])<br></td></tr
><tr
id=sl_svn496_227

><td class="source">                    except:<br></td></tr
><tr
id=sl_svn496_228

><td class="source">                        row[&#39;image&#39;] = graphics.Image.new(self.attrs[&#39;image_size&#39;])<br></td></tr
><tr
id=sl_svn496_229

><td class="source">                        row[&#39;image&#39;].clear(fill)<br></td></tr
><tr
id=sl_svn496_230

><td class="source">                        row[&#39;image&#39;].text((1,self.attrs[&#39;image_size&#39;][1]/2+self.attrs[&#39;font_height&#39;]/2),<br></td></tr
><tr
id=sl_svn496_231

><td class="source">                                          u&quot;X&quot;,<br></td></tr
><tr
id=sl_svn496_232

><td class="source">                                          fill=font_color,<br></td></tr
><tr
id=sl_svn496_233

><td class="source">                                          font=self.attrs[&#39;font_name&#39;])<br></td></tr
><tr
id=sl_svn496_234

><td class="source">                self._screen.blit(row[&#39;image&#39;],<br></td></tr
><tr
id=sl_svn496_235

><td class="source">                                  target=(self.images_xa,y-self.attrs[&#39;font_height&#39;]-1),<br></td></tr
><tr
id=sl_svn496_236

><td class="source">                                  source=((0,0),self.attrs[&#39;image_size&#39;]))<br></td></tr
><tr
id=sl_svn496_237

><td class="source">            #draw text<br></td></tr
><tr
id=sl_svn496_238

><td class="source">            yh = 0<br></td></tr
><tr
id=sl_svn496_239

><td class="source">            for line in row[&#39;text&#39;]:<br></td></tr
><tr
id=sl_svn496_240

><td class="source">                self._screen.text((xa,y+yh),<br></td></tr
><tr
id=sl_svn496_241

><td class="source">                                  line,fill=font_color,<br></td></tr
><tr
id=sl_svn496_242

><td class="source">                                  font=self.attrs[&#39;font_name&#39;])<br></td></tr
><tr
id=sl_svn496_243

><td class="source">                yh += self.attrs[&#39;font_height&#39;] + self.attrs[&#39;line_space&#39;]<br></td></tr
><tr
id=sl_svn496_244

><td class="source">            y += row[&#39;height&#39;]<br></td></tr
><tr
id=sl_svn496_245

><td class="source">            n += 1<br></td></tr
></table></pre>

<pre class="prettyprint lang-py"><table id="src_table_1"><tr
id=sl_svn496_246

><td class="source"><br></td></tr
><tr
id=sl_svn496_247

><td class="source">    def calculate_sel_view(self):<br></td></tr
><tr
id=sl_svn496_248

><td class="source">        &quot;&quot;&quot; Calculate the range of visible items<br></td></tr
><tr
id=sl_svn496_249

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_250

><td class="source">        n = self._selection_view[0]<br></td></tr
><tr
id=sl_svn496_251

><td class="source">        y = self.lstbox_ya<br></td></tr
><tr
id=sl_svn496_252

><td class="source">        while y &lt; self.lstbox_yb and n &lt; len(self.lstbox_items):<br></td></tr
><tr
id=sl_svn496_253

><td class="source">            y += self.lstbox_items[n][&#39;height&#39;]<br></td></tr
><tr
id=sl_svn496_254

><td class="source">            n += 1<br></td></tr
><tr
id=sl_svn496_255

><td class="source">        if y &gt;= self.lstbox_yb:<br></td></tr
><tr
id=sl_svn496_256

><td class="source">            # ensure all items in view are visible<br></td></tr
><tr
id=sl_svn496_257

><td class="source">            n -= 1<br></td></tr
><tr
id=sl_svn496_258

><td class="source">        # base index is 0<br></td></tr
><tr
id=sl_svn496_259

><td class="source">        self._selection_view[1] = n - 1<br></td></tr
><tr
id=sl_svn496_260

><td class="source">            <br></td></tr
><tr
id=sl_svn496_261

><td class="source">    def up_key(self):<br></td></tr
><tr
id=sl_svn496_262

><td class="source">        &quot;&quot;&quot; handle up navi key<br></td></tr
><tr
id=sl_svn496_263

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_264

><td class="source">        if self._current_sel &lt;= 0:<br></td></tr
><tr
id=sl_svn496_265

><td class="source">            return       <br></td></tr
><tr
id=sl_svn496_266

><td class="source">        n = self._current_sel - 1<br></td></tr
><tr
id=sl_svn496_267

><td class="source">        if n &lt; self._selection_view[0]:<br></td></tr
><tr
id=sl_svn496_268

><td class="source">            self._selection_view[0] -= 1<br></td></tr
><tr
id=sl_svn496_269

><td class="source">            self.calculate_sel_view()<br></td></tr
><tr
id=sl_svn496_270

><td class="source">        else:<br></td></tr
><tr
id=sl_svn496_271

><td class="source">            self._current_sel_in_view -= 1<br></td></tr
><tr
id=sl_svn496_272

><td class="source">            <br></td></tr
><tr
id=sl_svn496_273

><td class="source">        self._current_sel = self._current_sel_in_view + self._selection_view[0]<br></td></tr
><tr
id=sl_svn496_274

><td class="source">        self.redraw_list()               <br></td></tr
><tr
id=sl_svn496_275

><td class="source"><br></td></tr
><tr
id=sl_svn496_276

><td class="source">    def down_key(self):<br></td></tr
><tr
id=sl_svn496_277

><td class="source">        &quot;&quot;&quot; Handle down navi key<br></td></tr
><tr
id=sl_svn496_278

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_279

><td class="source">        if self._current_sel &gt;= (len(self.lstbox_items) - 1):<br></td></tr
><tr
id=sl_svn496_280

><td class="source">            return<br></td></tr
><tr
id=sl_svn496_281

><td class="source">        n = self._current_sel + 1<br></td></tr
><tr
id=sl_svn496_282

><td class="source">        if n &gt; self._selection_view[1]:<br></td></tr
><tr
id=sl_svn496_283

><td class="source">            # ensure that selected item in inside the view,<br></td></tr
><tr
id=sl_svn496_284

><td class="source">            # increasing the begining until it fits<br></td></tr
><tr
id=sl_svn496_285

><td class="source">            while n &gt; self._selection_view[1]:<br></td></tr
><tr
id=sl_svn496_286

><td class="source">                self._selection_view[0] += 1<br></td></tr
><tr
id=sl_svn496_287

><td class="source">                self.calculate_sel_view()<br></td></tr
><tr
id=sl_svn496_288

><td class="source">            self._current_sel_in_view = n - self._selection_view[0]<br></td></tr
><tr
id=sl_svn496_289

><td class="source">        else:<br></td></tr
><tr
id=sl_svn496_290

><td class="source">            self._current_sel_in_view += 1<br></td></tr
><tr
id=sl_svn496_291

><td class="source"><br></td></tr
><tr
id=sl_svn496_292

><td class="source">        self._current_sel = n<br></td></tr
><tr
id=sl_svn496_293

><td class="source">        self.redraw_list()            <br></td></tr
><tr
id=sl_svn496_294

><td class="source"><br></td></tr
><tr
id=sl_svn496_295

><td class="source">    def build_list(self,items):<br></td></tr
><tr
id=sl_svn496_296

><td class="source">        &quot;&quot;&quot; Pre-process the items list, splitting it in several lines that fit<br></td></tr
><tr
id=sl_svn496_297

><td class="source">            in the current listbox size<br></td></tr
><tr
id=sl_svn496_298

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_299

><td class="source">        if not self.attrs[&#39;images&#39;] or (len(self.attrs[&#39;images&#39;]) != len(items)):<br></td></tr
><tr
id=sl_svn496_300

><td class="source">            have_images = False<br></td></tr
><tr
id=sl_svn496_301

><td class="source">        else:<br></td></tr
><tr
id=sl_svn496_302

><td class="source">            have_images = True<br></td></tr
><tr
id=sl_svn496_303

><td class="source">        self.lstbox_items = []<br></td></tr
><tr
id=sl_svn496_304

><td class="source">        width = self.lstbox_xb - self.lstbox_xa<br></td></tr
><tr
id=sl_svn496_305

><td class="source">        n=0<br></td></tr
><tr
id=sl_svn496_306

><td class="source">        for item in items:<br></td></tr
><tr
id=sl_svn496_307

><td class="source">            # text: array with all lines for the current text, already splitted<br></td></tr
><tr
id=sl_svn496_308

><td class="source">            # num_line: len of array<br></td></tr
><tr
id=sl_svn496_309

><td class="source">            # height: how much height is necessary for displaying<br></td></tr
><tr
id=sl_svn496_310

><td class="source">            #           this text including line space<br></td></tr
><tr
id=sl_svn496_311

><td class="source">            reg = {}<br></td></tr
><tr
id=sl_svn496_312

><td class="source">            lines = item.split(u&#39;\n&#39;)<br></td></tr
><tr
id=sl_svn496_313

><td class="source">            reg[&#39;text&#39;] = []<br></td></tr
><tr
id=sl_svn496_314

><td class="source">            reg[&#39;num_lines&#39;] = 0<br></td></tr
><tr
id=sl_svn496_315

><td class="source">            reg[&#39;height&#39;] = 0<br></td></tr
><tr
id=sl_svn496_316

><td class="source">            for line in lines:<br></td></tr
><tr
id=sl_svn496_317

><td class="source">                splt_lines = self.split_text(line,width)<br></td></tr
><tr
id=sl_svn496_318

><td class="source">                reg[&#39;text&#39;] += splt_lines<br></td></tr
><tr
id=sl_svn496_319

><td class="source">                num_lines = len(splt_lines)<br></td></tr
><tr
id=sl_svn496_320

><td class="source">                reg[&#39;num_lines&#39;] += num_lines<br></td></tr
><tr
id=sl_svn496_321

><td class="source">                reg[&#39;height&#39;] += num_lines*(self.attrs[&#39;font_height&#39;] + \<br></td></tr
><tr
id=sl_svn496_322

><td class="source">                                            self.attrs[&#39;line_space&#39;])<br></td></tr
><tr
id=sl_svn496_323

><td class="source">            reg[&#39;file&#39;] = None<br></td></tr
><tr
id=sl_svn496_324

><td class="source">            if have_images:<br></td></tr
><tr
id=sl_svn496_325

><td class="source">                if self.attrs[&#39;images&#39;][n]:<br></td></tr
><tr
id=sl_svn496_326

><td class="source">                    reg[&#39;file&#39;] = self.attrs[&#39;images&#39;][n]<br></td></tr
><tr
id=sl_svn496_327

><td class="source">                    reg[&#39;image&#39;] = None<br></td></tr
><tr
id=sl_svn496_328

><td class="source">                    reg[&#39;height&#39;] = max(reg[&#39;height&#39;],self.attrs[&#39;image_size&#39;][1])<br></td></tr
><tr
id=sl_svn496_329

><td class="source">                <br></td></tr
><tr
id=sl_svn496_330

><td class="source">            self.lstbox_items.append(reg)<br></td></tr
><tr
id=sl_svn496_331

><td class="source">            n += 1<br></td></tr
><tr
id=sl_svn496_332

><td class="source">   <br></td></tr
><tr
id=sl_svn496_333

><td class="source">    def split_text(self, text, width):<br></td></tr
><tr
id=sl_svn496_334

><td class="source">        &quot;&quot;&quot; modified version of TextRenderer.chop for splitting text<br></td></tr
><tr
id=sl_svn496_335

><td class="source">            http://discussion.forum.nokia.com/forum/showthread.php?t=124666<br></td></tr
><tr
id=sl_svn496_336

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_337

><td class="source">        lines = []<br></td></tr
><tr
id=sl_svn496_338

><td class="source">        text_left = text<br></td></tr
><tr
id=sl_svn496_339

><td class="source">        while len(text_left) &gt; 0: <br></td></tr
><tr
id=sl_svn496_340

><td class="source">            bounding, to_right, fits = self.measure_text(text_left,<br></td></tr
><tr
id=sl_svn496_341

><td class="source">                                                         font=self.attrs[&#39;font_name&#39;],<br></td></tr
><tr
id=sl_svn496_342

><td class="source">                                                         maxwidth=width,<br></td></tr
><tr
id=sl_svn496_343

><td class="source">                                                         maxadvance=width)<br></td></tr
><tr
id=sl_svn496_344

><td class="source">            if fits &lt;= 0:<br></td></tr
><tr
id=sl_svn496_345

><td class="source">                lines.append(text_left)<br></td></tr
><tr
id=sl_svn496_346

><td class="source">                break<br></td></tr
><tr
id=sl_svn496_347

><td class="source"><br></td></tr
><tr
id=sl_svn496_348

><td class="source">            slice = text_left[0:fits]<br></td></tr
><tr
id=sl_svn496_349

><td class="source">            adjust = 0 # (preserve or not whitespaces at the end of the row)<br></td></tr
><tr
id=sl_svn496_350

><td class="source">        <br></td></tr
><tr
id=sl_svn496_351

><td class="source">            if len(slice) &lt; len(text_left):<br></td></tr
><tr
id=sl_svn496_352

><td class="source">                # find the separator character closest to the right<br></td></tr
><tr
id=sl_svn496_353

><td class="source">                rindex = -1<br></td></tr
><tr
id=sl_svn496_354

><td class="source">                for sep in self.attrs[&#39;line_break_chars&#39;]:<br></td></tr
><tr
id=sl_svn496_355

><td class="source">                    idx = slice.rfind(sep)<br></td></tr
><tr
id=sl_svn496_356

><td class="source">                    if idx &gt; rindex:<br></td></tr
><tr
id=sl_svn496_357

><td class="source">                        rindex = idx<br></td></tr
><tr
id=sl_svn496_358

><td class="source">                if rindex &gt; 0:<br></td></tr
><tr
id=sl_svn496_359

><td class="source">                    if slice[rindex] == u&#39; &#39;:<br></td></tr
><tr
id=sl_svn496_360

><td class="source">                        adjust = 1<br></td></tr
><tr
id=sl_svn496_361

><td class="source">                    slice = slice[0:rindex]<br></td></tr
><tr
id=sl_svn496_362

><td class="source"><br></td></tr
><tr
id=sl_svn496_363

><td class="source">            lines.append(slice)<br></td></tr
><tr
id=sl_svn496_364

><td class="source">            text_left = text_left[len(slice)+adjust:]<br></td></tr
><tr
id=sl_svn496_365

><td class="source">        <br></td></tr
><tr
id=sl_svn496_366

><td class="source">        return lines<br></td></tr
><tr
id=sl_svn496_367

><td class="source">    <br></td></tr
><tr
id=sl_svn496_368

><td class="source">    def event_list(self,ev):<br></td></tr
><tr
id=sl_svn496_369

><td class="source">        pass<br></td></tr
><tr
id=sl_svn496_370

><td class="source"><br></td></tr
><tr
id=sl_svn496_371

><td class="source">    def clear_list(self):<br></td></tr
><tr
id=sl_svn496_372

><td class="source">        &quot;&quot;&quot; Clear screen<br></td></tr
><tr
id=sl_svn496_373

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_374

><td class="source">        self._screen.clear(self.attrs[&#39;font_fill_color&#39;])<br></td></tr
><tr
id=sl_svn496_375

><td class="source">        self.blit(self._screen,<br></td></tr
><tr
id=sl_svn496_376

><td class="source">                  target=(self.attrs[&#39;position&#39;][0],self.attrs[&#39;position&#39;][1]),<br></td></tr
><tr
id=sl_svn496_377

><td class="source">                  source=((0,0),self.lstbox_size))<br></td></tr
><tr
id=sl_svn496_378

><td class="source"><br></td></tr
><tr
id=sl_svn496_379

><td class="source">    def current(self):<br></td></tr
><tr
id=sl_svn496_380

><td class="source">        &quot;&quot;&quot; Return the selected item<br></td></tr
><tr
id=sl_svn496_381

><td class="source">        &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_382

><td class="source">        return self._current_sel<br></td></tr
><tr
id=sl_svn496_383

><td class="source">     <br></td></tr
><tr
id=sl_svn496_384

><td class="source">class ExplorerDemo(object):<br></td></tr
><tr
id=sl_svn496_385

><td class="source">    &quot;&quot;&quot; Demo explorer class<br></td></tr
><tr
id=sl_svn496_386

><td class="source">    &quot;&quot;&quot;<br></td></tr
><tr
id=sl_svn496_387

><td class="source">    def __init__(self,init_dir = &quot;&quot;):       <br></td></tr
><tr
id=sl_svn496_388

><td class="source">        self.lock = e32.Ao_lock()<br></td></tr
><tr
id=sl_svn496_389

><td class="source">        app.title = u&quot;Explorer demo&quot;<br></td></tr
><tr
id=sl_svn496_390

><td class="source">        app.screen = &quot;full&quot;<br></td></tr
><tr
id=sl_svn496_391

><td class="source">        self.show_images = True        <br></td></tr
><tr
id=sl_svn496_392

><td class="source">        app.menu = [(u&quot;Hide images&quot;, lambda: self.images_menu(False)),<br></td></tr
><tr
id=sl_svn496_393

><td class="source">                    (u&quot;About&quot;, self.about),<br></td></tr
><tr
id=sl_svn496_394

><td class="source">                    (u&quot;Quit&quot;, self.close_app)]<br></td></tr
><tr
id=sl_svn496_395

><td class="source">        self.cur_dir = unicode(init_dir)<br></td></tr
><tr
id=sl_svn496_396

><td class="source">        if not os.path.exists(self.cur_dir):<br></td></tr
><tr
id=sl_svn496_397

><td class="source">            self.cur_dir = u&quot;&quot;<br></td></tr
><tr
id=sl_svn496_398

><td class="source">        self.fill_items()<br></td></tr
><tr
id=sl_svn496_399

><td class="source">        <br></td></tr
><tr
id=sl_svn496_400

><td class="source">        pos = (0,0) + sysinfo.display_pixels()<br></td></tr
><tr
id=sl_svn496_401

><td class="source">        self.listbox = CanvasListBox(items=self.items,<br></td></tr
><tr
id=sl_svn496_402

><td class="source">                                     cbk=self.item_selected,<br></td></tr
><tr
id=sl_svn496_403

><td class="source">                                     images=self.images,<br></td></tr
><tr
id=sl_svn496_404

><td class="source">                                     position=pos,<br></td></tr
><tr
id=sl_svn496_405

><td class="source">                                     margins=[6,2,2,2],<br></td></tr
><tr
id=sl_svn496_406

><td class="source">                                     selection_border_color=(124,104,238),<br></td></tr
><tr
id=sl_svn496_407

><td class="source">                                     image_size=(44,44),<br></td></tr
><tr
id=sl_svn496_408

><td class="source">                                     title=self.cur_dir)<br></td></tr
><tr
id=sl_svn496_409

><td class="source">        <br></td></tr
><tr
id=sl_svn496_410

><td class="source">        app.body = self.listbox<br></td></tr
><tr
id=sl_svn496_411

><td class="source">        self.lock.wait()<br></td></tr
><tr
id=sl_svn496_412

><td class="source">        <br></td></tr
><tr
id=sl_svn496_413

><td class="source">    def fill_items(self):<br></td></tr
><tr
id=sl_svn496_414

><td class="source">        if self.cur_dir == u&quot;&quot;:<br></td></tr
><tr
id=sl_svn496_415

><td class="source">            self.items = [ unicode(d + &quot;\\&quot;) for d in e32.drive_list() ]<br></td></tr
><tr
id=sl_svn496_416

><td class="source">            self.images = [None for d in self.items]<br></td></tr
><tr
id=sl_svn496_417

><td class="source">        else:<br></td></tr
><tr
id=sl_svn496_418

><td class="source">            entries = [ e.decode(&#39;utf-8&#39;)<br></td></tr
><tr
id=sl_svn496_419

><td class="source">                        for e in os.listdir( self.cur_dir.encode(&#39;utf-8&#39;) ) ]<br></td></tr
><tr
id=sl_svn496_420

><td class="source">            entries.sort()<br></td></tr
><tr
id=sl_svn496_421

><td class="source">            d = self.cur_dir<br></td></tr
><tr
id=sl_svn496_422

><td class="source">            dirs = []<br></td></tr
><tr
id=sl_svn496_423

><td class="source">            files = []<br></td></tr
><tr
id=sl_svn496_424

><td class="source">            dimages = []<br></td></tr
><tr
id=sl_svn496_425

><td class="source">            fimages = []<br></td></tr
><tr
id=sl_svn496_426

><td class="source">            for e in entries:<br></td></tr
><tr
id=sl_svn496_427

><td class="source">                f = os.path.join(d,e)<br></td></tr
><tr
id=sl_svn496_428

><td class="source">                if os.path.isdir(f.encode(&#39;utf-8&#39;)):<br></td></tr
><tr
id=sl_svn496_429

><td class="source">                    dirs.append(e.upper())<br></td></tr
><tr
id=sl_svn496_430

><td class="source">                    dimages.append(None)<br></td></tr
><tr
id=sl_svn496_431

><td class="source">                elif os.path.isfile(f.encode(&#39;utf-8&#39;)):<br></td></tr
><tr
id=sl_svn496_432

><td class="source">                    desc = e.lower() + &quot;\n&quot;<br></td></tr
><tr
id=sl_svn496_433

><td class="source">                    desc += &quot;%d bytes&quot; % os.path.getsize(f)<br></td></tr
><tr
id=sl_svn496_434

><td class="source">                    files.append(desc)<br></td></tr
><tr
id=sl_svn496_435

><td class="source">                    if f.endswith(&quot;.jpg&quot;) or f.endswith(&quot;.png&quot;) or f.endswith(&quot;.gif&quot;):<br></td></tr
><tr
id=sl_svn496_436

><td class="source">                        fimages.append(f)<br></td></tr
><tr
id=sl_svn496_437

><td class="source">                    else:<br></td></tr
><tr
id=sl_svn496_438

><td class="source">                        fimages.append(None)<br></td></tr
><tr
id=sl_svn496_439

><td class="source">            dirs.insert(0, u&quot;..&quot; )<br></td></tr
><tr
id=sl_svn496_440

><td class="source">            dimages.insert(0,None)<br></td></tr
><tr
id=sl_svn496_441

><td class="source">            self.items = dirs + files<br></td></tr
><tr
id=sl_svn496_442

><td class="source">            self.images = dimages + fimages       <br></td></tr
><tr
id=sl_svn496_443

><td class="source"><br></td></tr
><tr
id=sl_svn496_444

><td class="source">    def images_menu(self,val):<br></td></tr
><tr
id=sl_svn496_445

><td class="source">        self.show_images = val<br></td></tr
><tr
id=sl_svn496_446

><td class="source">        menu = []<br></td></tr
><tr
id=sl_svn496_447

><td class="source">        if val:<br></td></tr
><tr
id=sl_svn496_448

><td class="source">            menu += [(u&quot;Hide images&quot;, lambda: self.images_menu(False))]<br></td></tr
><tr
id=sl_svn496_449

><td class="source">        else:<br></td></tr
><tr
id=sl_svn496_450

><td class="source">            menu += [(u&quot;Show images&quot;, lambda: self.images_menu(True))]<br></td></tr
><tr
id=sl_svn496_451

><td class="source">        menu += [(u&quot;About&quot;, self.about),<br></td></tr
><tr
id=sl_svn496_452

><td class="source">                 (u&quot;Quit&quot;, self.close_app)]<br></td></tr
><tr
id=sl_svn496_453

><td class="source">        app.menu = menu<br></td></tr
><tr
id=sl_svn496_454

><td class="source">        self.update_list()<br></td></tr
><tr
id=sl_svn496_455

><td class="source">                    <br></td></tr
><tr
id=sl_svn496_456

><td class="source">    def item_selected(self):<br></td></tr
><tr
id=sl_svn496_457

><td class="source">        item = self.listbox.current()<br></td></tr
><tr
id=sl_svn496_458

><td class="source">        f = self.items[item]<br></td></tr
><tr
id=sl_svn496_459

><td class="source">        self.update_list(f)<br></td></tr
></table></pre>

<pre class="prettyprint lang-py"><table id="src_table_2"><tr
id=sl_svn496_460

><td class="source"><br></td></tr
><tr
id=sl_svn496_461

><td class="source">    def update_list(self,f=u&quot;&quot;):<br></td></tr
><tr
id=sl_svn496_462

><td class="source">        if f:<br></td></tr
><tr
id=sl_svn496_463

><td class="source">            d = os.path.abspath( os.path.join(self.cur_dir,f) )<br></td></tr
><tr
id=sl_svn496_464

><td class="source">        else:<br></td></tr
><tr
id=sl_svn496_465

><td class="source">            d = self.cur_dir<br></td></tr
><tr
id=sl_svn496_466

><td class="source">        if os.path.isdir(d.encode(&#39;utf-8&#39;)):<br></td></tr
><tr
id=sl_svn496_467

><td class="source">            if f == u&quot;..&quot; and len(self.cur_dir) == 3:<br></td></tr
><tr
id=sl_svn496_468

><td class="source">                self.cur_dir = u&quot;&quot;<br></td></tr
><tr
id=sl_svn496_469

><td class="source">            else:<br></td></tr
><tr
id=sl_svn496_470

><td class="source">                self.cur_dir = d <br></td></tr
><tr
id=sl_svn496_471

><td class="source">            self.fill_items()<br></td></tr
><tr
id=sl_svn496_472

><td class="source">            attrs = self.listbox.get_config()<br></td></tr
><tr
id=sl_svn496_473

><td class="source">            attrs[&#39;items&#39;] = self.items<br></td></tr
><tr
id=sl_svn496_474

><td class="source">            attrs[&#39;title&#39;] = u&quot; &quot; + self.cur_dir<br></td></tr
><tr
id=sl_svn496_475

><td class="source">            if self.show_images:<br></td></tr
><tr
id=sl_svn496_476

><td class="source">                attrs[&#39;images&#39;] = self.images<br></td></tr
><tr
id=sl_svn496_477

><td class="source">                attrs[&#39;image_size&#39;] = (44,44)<br></td></tr
><tr
id=sl_svn496_478

><td class="source">            else:<br></td></tr
><tr
id=sl_svn496_479

><td class="source">                attrs[&#39;images&#39;] = []<br></td></tr
><tr
id=sl_svn496_480

><td class="source">                <br></td></tr
><tr
id=sl_svn496_481

><td class="source">            self.listbox.reconfigure(attrs)<br></td></tr
><tr
id=sl_svn496_482

><td class="source"><br></td></tr
><tr
id=sl_svn496_483

><td class="source">    def about(self):<br></td></tr
><tr
id=sl_svn496_484

><td class="source">        note(u&quot;Explorer demo by Marcelo Barros (marcelobarrosalmeida@gmail.com)&quot;,&quot;info&quot;)<br></td></tr
><tr
id=sl_svn496_485

><td class="source">        <br></td></tr
><tr
id=sl_svn496_486

><td class="source">    def close_app(self):<br></td></tr
><tr
id=sl_svn496_487

><td class="source">        self.lock.signal()<br></td></tr
><tr
id=sl_svn496_488

><td class="source">        app.set_exit()<br></td></tr
><tr
id=sl_svn496_489

><td class="source"><br></td></tr
><tr
id=sl_svn496_490

><td class="source">if __name__ == &quot;__main__&quot;:<br></td></tr
><tr
id=sl_svn496_491

><td class="source">    ExplorerDemo()<br></td></tr
><tr
id=sl_svn496_492

><td class="source"><br></td></tr
><tr
id=sl_svn496_493

><td class="source"><br></td></tr
></table></pre>

<pre class="prettyprint"><table width="100%"><tr class="cursor_stop cursor_hidden"><td></td></tr></table></pre>
</td>
</tr></table>
<script type="text/javascript">
 var lineNumUnderMouse = -1;
 
 function gutterOver(num) {
 gutterOut();
 var newTR = document.getElementById('gr_svn496_' + num);
 if (newTR) {
 newTR.className = 'undermouse';
 }
 lineNumUnderMouse = num;
 }
 function gutterOut() {
 if (lineNumUnderMouse != -1) {
 var oldTR = document.getElementById(
 'gr_svn496_' + lineNumUnderMouse);
 if (oldTR) {
 oldTR.className = '';
 }
 lineNumUnderMouse = -1;
 }
 }
 var numsGenState = {table_base_id: 'nums_table_'};
 var srcGenState = {table_base_id: 'src_table_'};
 var alignerRunning = false;
 var startOver = false;
 function setLineNumberHeights() {
 if (alignerRunning) {
 startOver = true;
 return;
 }
 numsGenState.chunk_id = 0;
 numsGenState.table = document.getElementById('nums_table_0');
 numsGenState.row_num = 0;
 srcGenState.chunk_id = 0;
 srcGenState.table = document.getElementById('src_table_0');
 srcGenState.row_num = 0;
 alignerRunning = true;
 continueToSetLineNumberHeights();
 }
 function rowGenerator(genState) {
 if (genState.row_num < genState.table.rows.length) {
 var currentRow = genState.table.rows[genState.row_num];
 genState.row_num++;
 return currentRow;
 }
 var newTable = document.getElementById(
 genState.table_base_id + (genState.chunk_id + 1));
 if (newTable) {
 genState.chunk_id++;
 genState.row_num = 0;
 genState.table = newTable;
 return genState.table.rows[0];
 }
 return null;
 }
 var MAX_ROWS_PER_PASS = 1000;
 function continueToSetLineNumberHeights() {
 var rowsInThisPass = 0;
 var numRow = 1;
 var srcRow = 1;
 while (numRow && srcRow && rowsInThisPass < MAX_ROWS_PER_PASS) {
 numRow = rowGenerator(numsGenState);
 srcRow = rowGenerator(srcGenState);
 rowsInThisPass++;
 if (numRow && srcRow) {
 if (numRow.offsetHeight != srcRow.offsetHeight) {
 numRow.firstChild.style.height = srcRow.offsetHeight + 'px';
 }
 }
 }
 if (rowsInThisPass >= MAX_ROWS_PER_PASS) {
 setTimeout(continueToSetLineNumberHeights, 10);
 } else {
 alignerRunning = false;
 if (startOver) {
 startOver = false;
 setTimeout(setLineNumberHeights, 500);
 }
 }
 }
 // Do 2 complete passes, because there can be races
 // between this code and prettify.
 startOver = true;
 setTimeout(setLineNumberHeights, 250);
 window.onresize = setLineNumberHeights;
</script>

 
 
 <div id="log">
 <div style="text-align:right">
 <a class="ifCollapse" href="#" onclick="_toggleMeta('', 'p', 'wordmobi', this)">Show details</a>
 <a class="ifExpand" href="#" onclick="_toggleMeta('', 'p', 'wordmobi', this)">Hide details</a>
 </div>
 <div class="ifExpand">
 
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="changelog">
 <p>Change log</p>
 <div>
 <a href="/p/wordmobi/source/detail?spec=svn704&r=496">r496</a>
 by marcelobarrosalmeida
 on Apr 10, 2009
 &nbsp; <a href="/p/wordmobi/source/diff?spec=svn704&r=496&amp;format=side&amp;path=/trunk/canvaslistbox/canvaslistbox.py&amp;old_path=/trunk/canvaslistbox/canvaslistbox.py&amp;old=">Diff</a>
 </div>
 <pre>Renaming para canvaslistbox again</pre>
 </div>
 
 
 
 
 
 
 <script type="text/javascript">
 var detail_url = '/p/wordmobi/source/detail?r=496&spec=svn704';
 var publish_url = '/p/wordmobi/source/detail?r=496&spec=svn704#publish';
 // describe the paths of this revision in javascript.
 var changed_paths = [];
 var changed_urls = [];
 
 changed_paths.push('/trunk/canvaslistbox/CanvasLB1.0.0.sis');
 changed_urls.push('/p/wordmobi/source/browse/trunk/canvaslistbox/CanvasLB1.0.0.sis?r=496&spec=svn704');
 
 
 changed_paths.push('/trunk/canvaslistbox/canvaslistbox.py');
 changed_urls.push('/p/wordmobi/source/browse/trunk/canvaslistbox/canvaslistbox.py?r=496&spec=svn704');
 
 var selected_path = '/trunk/canvaslistbox/canvaslistbox.py';
 
 
 changed_paths.push('/trunk/canvaslistbox/create_sis.bat');
 changed_urls.push('/p/wordmobi/source/browse/trunk/canvaslistbox/create_sis.bat?r=496&spec=svn704');
 
 
 changed_paths.push('/trunk/canvaslistbox/explorer.py');
 changed_urls.push('/p/wordmobi/source/browse/trunk/canvaslistbox/explorer.py?r=496&spec=svn704');
 
 
 function getCurrentPageIndex() {
 for (var i = 0; i < changed_paths.length; i++) {
 if (selected_path == changed_paths[i]) {
 return i;
 }
 }
 }
 function getNextPage() {
 var i = getCurrentPageIndex();
 if (i < changed_paths.length - 1) {
 return changed_urls[i + 1];
 }
 return null;
 }
 function getPreviousPage() {
 var i = getCurrentPageIndex();
 if (i > 0) {
 return changed_urls[i - 1];
 }
 return null;
 }
 function gotoNextPage() {
 var page = getNextPage();
 if (!page) {
 page = detail_url;
 }
 window.location = page;
 }
 function gotoPreviousPage() {
 var page = getPreviousPage();
 if (!page) {
 page = detail_url;
 }
 window.location = page;
 }
 function gotoDetailPage() {
 window.location = detail_url;
 }
 function gotoPublishPage() {
 window.location = publish_url;
 }
</script>
 
 <style type="text/css">
 #review_nav {
 border-top: 3px solid white;
 padding-top: 6px;
 margin-top: 1em;
 }
 #review_nav td {
 vertical-align: middle;
 }
 #review_nav select {
 margin: .5em 0;
 }
 </style>
 <div id="review_nav">
 <table><tr><td>Go to:&nbsp;</td><td>
 <select name="files_in_rev" onchange="window.location=this.value">
 
 <option value="/p/wordmobi/source/browse/trunk/canvaslistbox/CanvasLB1.0.0.sis?r=496&amp;spec=svn704"
 
 >.../canvaslistbox/CanvasLB1.0.0.sis</option>
 
 <option value="/p/wordmobi/source/browse/trunk/canvaslistbox/canvaslistbox.py?r=496&amp;spec=svn704"
 selected="selected"
 >...k/canvaslistbox/canvaslistbox.py</option>
 
 <option value="/p/wordmobi/source/browse/trunk/canvaslistbox/create_sis.bat?r=496&amp;spec=svn704"
 
 >/trunk/canvaslistbox/create_sis.bat</option>
 
 <option value="/p/wordmobi/source/browse/trunk/canvaslistbox/explorer.py?r=496&amp;spec=svn704"
 
 >/trunk/canvaslistbox/explorer.py</option>
 
 </select>
 </td></tr></table>
 
 
 



 <div style="white-space:nowrap">
 Project members,
 <a href="https://www.google.com/accounts/ServiceLogin?service=code&amp;ltmpl=phosting&amp;continue=http%3A%2F%2Fcode.google.com%2Fp%2Fwordmobi%2Fsource%2Fbrowse%2Ftrunk%2Fcanvaslistbox%2Fcanvaslistbox.py&amp;followup=http%3A%2F%2Fcode.google.com%2Fp%2Fwordmobi%2Fsource%2Fbrowse%2Ftrunk%2Fcanvaslistbox%2Fcanvaslistbox.py"
 >sign in</a> to write a code review</div>


 
 </div>
 
 
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="older_bubble">
 <p>Older revisions</p>
 
 <a href="/p/wordmobi/source/list?path=/trunk/canvaslistbox/canvaslistbox.py&start=496">All revisions of this file</a>
 </div>
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 <div class="pmeta_bubble_bg" style="border:1px solid white">
 <div class="round4"></div>
 <div class="round2"></div>
 <div class="round1"></div>
 <div class="box-inner">
 <div id="fileinfo_bubble">
 <p>File info</p>
 
 <div>Size: 19961 bytes,
 493 lines</div>
 
 <div><a href="http://wordmobi.googlecode.com/svn/trunk/canvaslistbox/canvaslistbox.py">View raw file</a></div>
 </div>
 
 <div id="props">
 <p>File properties</p>
 <dl>
 
 <dt>svn:eol-style</dt>
 <dd>native</dd>
 
 </dl>
 </div>
 
 </div>
 <div class="round1"></div>
 <div class="round2"></div>
 <div class="round4"></div>
 </div>
 </div>
 </div>


</div>
</div>

 <script src="http://www.gstatic.com/codesite/ph/7642550995449508181/js/prettify/prettify.js"></script>

<script type="text/javascript">prettyPrint();</script>

<script src="http://www.gstatic.com/codesite/ph/7642550995449508181/js/source_file_scripts.js"></script>

 <script type="text/javascript" src="http://kibbles.googlecode.com/files/kibbles-1.3.1.comp.js"></script>
 <script type="text/javascript">
 var lastStop = null;
 var initilized = false;
 
 function updateCursor(next, prev) {
 if (prev && prev.element) {
 prev.element.className = 'cursor_stop cursor_hidden';
 }
 if (next && next.element) {
 next.element.className = 'cursor_stop cursor';
 lastStop = next.index;
 }
 }
 
 function pubRevealed(data) {
 updateCursorForCell(data.cellId, 'cursor_stop cursor_hidden');
 if (initilized) {
 reloadCursors();
 }
 }
 
 function draftRevealed(data) {
 updateCursorForCell(data.cellId, 'cursor_stop cursor_hidden');
 if (initilized) {
 reloadCursors();
 }
 }
 
 function draftDestroyed(data) {
 updateCursorForCell(data.cellId, 'nocursor');
 if (initilized) {
 reloadCursors();
 }
 }
 function reloadCursors() {
 kibbles.skipper.reset();
 loadCursors();
 if (lastStop != null) {
 kibbles.skipper.setCurrentStop(lastStop);
 }
 }
 // possibly the simplest way to insert any newly added comments
 // is to update the class of the corresponding cursor row,
 // then refresh the entire list of rows.
 function updateCursorForCell(cellId, className) {
 var cell = document.getElementById(cellId);
 // we have to go two rows back to find the cursor location
 var row = getPreviousElement(cell.parentNode);
 row.className = className;
 }
 // returns the previous element, ignores text nodes.
 function getPreviousElement(e) {
 var element = e.previousSibling;
 if (element.nodeType == 3) {
 element = element.previousSibling;
 }
 if (element && element.tagName) {
 return element;
 }
 }
 function loadCursors() {
 // register our elements with skipper
 var elements = CR_getElements('*', 'cursor_stop');
 var len = elements.length;
 for (var i = 0; i < len; i++) {
 var element = elements[i]; 
 element.className = 'cursor_stop cursor_hidden';
 kibbles.skipper.append(element);
 }
 }
 function toggleComments() {
 CR_toggleCommentDisplay();
 reloadCursors();
 }
 function keysOnLoadHandler() {
 // setup skipper
 kibbles.skipper.addStopListener(
 kibbles.skipper.LISTENER_TYPE.PRE, updateCursor);
 // Set the 'offset' option to return the middle of the client area
 // an option can be a static value, or a callback
 kibbles.skipper.setOption('padding_top', 50);
 // Set the 'offset' option to return the middle of the client area
 // an option can be a static value, or a callback
 kibbles.skipper.setOption('padding_bottom', 100);
 // Register our keys
 kibbles.skipper.addFwdKey("n");
 kibbles.skipper.addRevKey("p");
 kibbles.keys.addKeyPressListener(
 'u', function() { window.location = detail_url; });
 kibbles.keys.addKeyPressListener(
 'r', function() { window.location = detail_url + '#publish'; });
 
 kibbles.keys.addKeyPressListener('j', gotoNextPage);
 kibbles.keys.addKeyPressListener('k', gotoPreviousPage);
 
 
 }
 window.onload = function() {keysOnLoadHandler();};
 </script>

<!-- code review support -->
<script src="http://www.gstatic.com/codesite/ph/7642550995449508181/js/code_review_scripts.js"></script>
<script type="text/javascript">
 
 // the comment form template
 var form = '<div class="draft"><div class="header"><span class="title">Draft comment:</span></div>' +
 '<div class="body"><form onsubmit="return false;"><textarea id="$ID">$BODY</textarea><br>$ACTIONS</form></div>' +
 '</div>';
 // the comment "plate" template used for both draft and published comment "plates".
 var draft_comment = '<div class="draft" ondblclick="$ONDBLCLICK">' +
 '<div class="header"><span class="title">Draft comment:</span><span class="actions">$ACTIONS</span></div>' +
 '<pre id="$ID" class="body">$BODY</pre>' +
 '</div>';
 var published_comment = '<div class="published">' +
 '<div class="header"><span class="title"><a href="$PROFILE_URL">$AUTHOR:</a></span><div>' +
 '<pre id="$ID" class="body">$BODY</pre>' +
 '</div>';

 function showPublishInstructions() {
 var element = document.getElementById('review_instr');
 if (element) {
 element.className = 'opened';
 }
 }
 function revsOnLoadHandler() {
 // register our source container with the commenting code
 var paths = {'svn496': '/trunk/canvaslistbox/canvaslistbox.py'}
 CR_setup('', 'p', 'wordmobi', '', 'svn704', paths,
 '', CR_BrowseIntegrationFactory);
 // register our hidden ui elements with the code commenting code ui builder.
 CR_registerLayoutElement('form', form);
 CR_registerLayoutElement('draft_comment', draft_comment);
 CR_registerLayoutElement('published_comment', published_comment);
 
 CR_registerActivityListener(CR_ACTIVITY_TYPE.REVEAL_DRAFT_PLATE, showPublishInstructions);
 
 CR_registerActivityListener(CR_ACTIVITY_TYPE.REVEAL_PUB_PLATE, pubRevealed);
 CR_registerActivityListener(CR_ACTIVITY_TYPE.REVEAL_DRAFT_PLATE, draftRevealed);
 CR_registerActivityListener(CR_ACTIVITY_TYPE.DISCARD_DRAFT_COMMENT, draftDestroyed);
 
 
 
 
 
 
 
 
 
 var initilized = true;
 reloadCursors();
 }
 window.onload = function() {keysOnLoadHandler(); revsOnLoadHandler();};
</script>
<script type="text/javascript" src="http://www.gstatic.com/codesite/ph/7642550995449508181/js/dit_scripts.js"></script>

 
 
 <script type="text/javascript" src="http://www.gstatic.com/codesite/ph/7642550995449508181/js/core_scripts_20081103.js"></script>
 <script type="text/javascript" src="/js/codesite_product_dictionary_ph.pack.04102009.js"></script>
 </div>
<div id="footer" dir="ltr">
 
 <div class="text">
 
 &copy;2010 Google -
 <a href="/projecthosting/terms.html">Terms</a> -
 <a href="http://www.google.com/privacy.html">Privacy</a> -
 <a href="/p/support/">Project Hosting Help</a>
 
 </div>
</div>

 <div class="hostedBy" style="margin-top: -20px;">
 <span style="vertical-align: top;">Powered by <a href="http://code.google.com/projecthosting/">Google Project Hosting</a></span>
 </div>
 
 


 
 </body>
</html>

