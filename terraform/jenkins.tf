# terraform/jenkins.tf

resource "helm_release" "jenkins" {
  name       = "jenkins"
  chart      = "${path.module}/../helm/jenkins"
  namespace  = "default"

  depends_on = [aws_eks_node_group.main]

  # secrets injected at apply time, never committed to Git
#   set_sensitive {
#     name  = "controller.env[6].value" # GITHUB_TOKEN, etc — better to restructure values.yaml so these are separate keys
#     value = var.github_token
#   }
}
