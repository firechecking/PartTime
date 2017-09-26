<%@page import="java.io.BufferedReader"%>  
<%@page import="java.io.FileReader"%>  
<%@page import="java.io.File"%>  
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">  
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">  
<title>智能机器人组文档目录</title>
</head>  
<body>  
    <%  
    	StringBuffer strB = new StringBuffer();   //strB用来存储jsp.txt文件里的内容  
		
        String sessionPath = request.getSession().getServletContext().getRealPath("/");
       	File sessionfile = new File(sessionPath);
       	String webPath =sessionfile.getParent();
        File webFile = new File(webPath);
        //String[] files = webFile.list();
		File[] files = webFile.listFiles();
		for (File file:files){
			if (file.isDirectory()){
				String filename = file.getName();
        		if (filename.startsWith("sphinx-docs-"))
        			strB.append("<a href=../"+filename+">"+filename.substring(12)+"</a>").append("<br>");
			}	
		}
    %>

<h1 align= center>智能机器人组文档目录</h1>
<hr style="height:10px;border:none;border-top:10px groove skyblue;" />

<hr style="height:1px;border:none;border-top:1px dashed #0066CC;" />
<h3>公网服务器</h3>
<%=strB %>
<hr style="height:1px;border:none;border-top:1px dashed #0066CC;" />
</body>  
</html>  