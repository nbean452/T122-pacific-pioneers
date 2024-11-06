import { Button } from "@components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@components/ui/card";

const HomePage = () => {
  // print env
  const endpoint = process.env.NEXT_PUBLIC_API_ENDPOINT;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Title</CardTitle>
      </CardHeader>

      <CardContent>
        <p>{endpoint}</p>
      </CardContent>

      <CardFooter className="flex justify-between">
        <Button variant="outline">Outline variant</Button>
        <Button>Default variant</Button>
      </CardFooter>
    </Card>
  );
};

export default HomePage;
