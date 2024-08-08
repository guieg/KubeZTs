#kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-deployment.yaml
#kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-service.yaml
#kubectl apply -f https://k8s.io/examples/application/guestbook/redis-follower-service.yaml
#kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-deployment.yaml
#kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-service.yaml

kubectl apply -f https://raw.githubusercontent.com/dockersamples/example-voting-app/main/k8s-specifications/db-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/dockersamples/example-voting-app/main/k8s-specifications/db-service.yaml
kubectl apply -f https://raw.githubusercontent.com/dockersamples/example-voting-app/main/k8s-specifications/redis-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/dockersamples/example-voting-app/main/k8s-specifications/redis-service.yaml
kubectl apply -f https://raw.githubusercontent.com/dockersamples/example-voting-app/main/k8s-specifications/result-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/dockersamples/example-voting-app/main/k8s-specifications/result-service.yaml
kubectl apply -f https://raw.githubusercontent.com/dockersamples/example-voting-app/main/k8s-specifications/vote-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/dockersamples/example-voting-app/main/k8s-specifications/vote-service.yaml
kubectl apply -f https://raw.githubusercontent.com/dockersamples/example-voting-app/main/k8s-specifications/worker-deployment.yaml
