#include <array>
#include <algorithm>

#include <likwid.h>

template <std::size_t N>
std::array<double,N>
matvec (const std::array<double,N*N>& matrix, const std::array<double,N>& vector)
{
  std::array<double,N> result;
  auto&& multiindex = [](const std::size_t i0, const std::size_t i1){return i0 + N*i1;};
  for (std::size_t m=0; m<N; ++m)
    for (std::size_t n=0; n<N; ++n)
      result[m] += matrix[multiindex(m,n)] * vector[n];
  return result;
}

int main()
{
  LIKWID_MARKER_INIT;
  constexpr std::size_t N=100;
  std::array<double,N> vector;
  std::array<double,N*N> matrix;

  auto&& gen_rand = [](){return static_cast<double>(std::rand()/RAND_MAX);};
  std::generate (vector.begin(), vector.end(), gen_rand);
  std::generate (matrix.begin(), matrix.end(), gen_rand);

  LIKWID_MARKER_START("matvec");
  auto result {matvec (matrix, vector)};
  LIKWID_MARKER_STOP("matvec");

  LIKWID_MARKER_CLOSE;
  return result.back();
}
