import unittest
import subprocess
import os

class TestCompilerEndToEnd(unittest.TestCase):

    def _run_compiler(self, source_code):
        # Escreve o código fonte em um arquivo temporário
        temp_file_path = "temp_test_code.charmeleon"
        with open(temp_file_path, "w") as f:
            f.write(source_code)

        # Executa o compilador como um subprocesso
        result = subprocess.run(
            ["python3.11", "main.py", temp_file_path], # Agora chama main.py
            capture_output=True,
            text=True,
            cwd="/home/ubuntu/charmeleon_compiler"
        )

        # Remove o arquivo temporário
        os.remove(temp_file_path)

        return result

    def test_if_else_statement(self):
        source_code = """
        func main() {
            var x = 10;
            if (x > 5) {
                print("maior");
            } else {
                print("menor");
            }
        }
        """
        compiler_result = self._run_compiler(source_code)
        self.assertIn("if x > 5:", compiler_result.stdout)
        self.assertIn("print(\"maior\")", compiler_result.stdout)
        self.assertIn("else:", compiler_result.stdout)
        self.assertIn("print(\"menor\")", compiler_result.stdout)

    def test_for_loop(self):
        source_code = """
        func main() {
            for (var i = 0; i < 3; i = i + 1) {
                print(i);
            }
        }
        """
        compiler_result = self._run_compiler(source_code)
        self.assertIn("while i < 3:", compiler_result.stdout)
        self.assertIn("print(i)", compiler_result.stdout)
        self.assertIn("i = i + 1", compiler_result.stdout)

    def test_while_loop(self):
        source_code = """
        func main() {
            var x = 3;
            while (x > 0) {
                print(x);
                x = x - 1;
            }
        }
        """
        compiler_result = self._run_compiler(source_code)
        self.assertIn("while x > 0:", compiler_result.stdout)
        self.assertIn("print(x)", compiler_result.stdout)
        self.assertIn("x = x - 1", compiler_result.stdout)

    def test_sast_injection_vulnerability(self):
        source_code = """
        func main() {
            var user_input = "admin";
            var query = "SELECT * FROM users WHERE name = \'" + user_input + "\'";
            print(query);
        }
        """
        compiler_result = self._run_compiler(source_code)
        # SAST results are now in stderr
        self.assertIn("PotentialInjection", compiler_result.stderr)

    def test_dead_code_elimination(self):
        source_code = """
        func main() {
            var x = 10;
            var y = 20; # Dead code
            print(x);
        }
        """
        compiler_result = self._run_compiler(source_code)
        # Verificamos o IR otimizado no stderr
        self.assertNotIn("ASSIGN y, 20", compiler_result.stderr)

if __name__ == "__main__":
    unittest.main()


