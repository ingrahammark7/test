from flask import Flask, Response

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Fractal Terrain</title>
  <style>
    body { margin: 0; overflow: hidden; background: #000; }
    canvas { display: block; }
  </style>
</head>
<body>
  <script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>
  <script>
    let scene = new THREE.Scene();
    let camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    let renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    let geometry = new THREE.PlaneGeometry(100, 100, 128, 128);
    let material = new THREE.MeshStandardMaterial({ color: 0x2288ff, wireframe: false, flatShading: true });
    let plane = new THREE.Mesh(geometry, material);
    plane.rotation.x = -Math.PI / 2;
    scene.add(plane);

    let light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(10, 10, 10);
    scene.add(light);

    let clock = new THREE.Clock();

    function updateTerrain(time) {
      let verts = geometry.attributes.position;
      for (let i = 0; i < verts.count; i++) {
        let x = verts.getX(i);
        let y = verts.getY(i);
        let z = Math.sin(x * 0.2 + time) * Math.cos(y * 0.2 + time) * 3;
        verts.setZ(i, z);
      }
      verts.needsUpdate = true;
      geometry.computeVertexNormals();
    }

    camera.position.set(0, 15, 30);
    camera.lookAt(0, 0, 0);

    function animate() {
      requestAnimationFrame(animate);
      let time = clock.getElapsedTime();
      updateTerrain(time);
      renderer.render(scene, camera);
    }

    animate();
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return Response(html, mimetype='text/html')

if __name__ == "__main__":
    app.run(debug=False)