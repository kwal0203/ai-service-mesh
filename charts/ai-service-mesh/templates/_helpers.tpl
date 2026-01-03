{{- define "ai-service-mesh.fullname" -}}
{{- printf "%s" .Release.Name -}}
{{- end -}}

{{- define "ai-service-mesh.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}
