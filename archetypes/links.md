---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
expiryDate: {{ now.AddDate 0 0 7}}
images: null
layout: links
linkType: null
linkTitle: "{{ replace .Name "-" " " | title }}"
publishDate: {{ .Date }}
linkurl: 
weight: 0
---
